import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np
import logging
import time
from datetime import datetime

from config import (
    MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER, MT5_PATH, TIMEFRAME,
    EMA_FAST, EMA_MEDIUM, EMA_SLOW, RSI_PERIOD,
    MACD_FAST, MACD_SLOW, MACD_SIGNAL, ATR_PERIOD, ADX_PERIOD,
    BOLLINGER_PERIOD, BOLLINGER_STD_DEV, DONCHIAN_PERIOD
)

logger = logging.getLogger(__name__)

class DataEngine:
    def __init__(self):
        self.connected = False

    def connect(self):
        """Connect to the MetaTrader 5 terminal."""
        if not mt5.initialize(path=MT5_PATH) if MT5_PATH else mt5.initialize():
            logger.error("initialize() failed, error code = %s", mt5.last_error())
            return False

        if not mt5.login(MT5_ACCOUNT, password=MT5_PASSWORD, server=MT5_SERVER):
            logger.error("login() failed, error code = %s", mt5.last_error())
            return False

        self.connected = True
        logger.info(f"Connected to MT5 account {MT5_ACCOUNT}")
        return True

    def disconnect(self):
        """Disconnect from the MetaTrader 5 terminal."""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")

    def _get_timeframe(self, tf_minutes):
        """Map minutes to MT5 timeframe constants."""
        if tf_minutes == 1:
            return mt5.TIMEFRAME_M1
        elif tf_minutes == 5:
            return mt5.TIMEFRAME_M5
        elif tf_minutes == 15:
            return mt5.TIMEFRAME_M15
        elif tf_minutes == 30:
            return mt5.TIMEFRAME_M30
        elif tf_minutes == 60:
            return mt5.TIMEFRAME_H1
        elif tf_minutes == 240:
            return mt5.TIMEFRAME_H4
        elif tf_minutes == 1440:
            return mt5.TIMEFRAME_D1
        return mt5.TIMEFRAME_M15

    def fetch_data(self, symbol, timeframe=TIMEFRAME, num_candles=500):
        """Fetch OHLCV data from MT5."""
        if not self.connected:
            if not self.connect():
                return None

        tf = self._get_timeframe(timeframe)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, num_candles)

        if rates is None or len(rates) == 0:
            logger.error(f"Failed to fetch data for {symbol}")
            return None

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        return df

    def compute_indicators(self, df):
        """Calculate technical indicators required by the strategies."""
        if df is None or len(df) < EMA_SLOW:
            return df

        # EMAs
        df['EMA_20'] = ta.ema(df['close'], length=EMA_FAST)
        df['EMA_50'] = ta.ema(df['close'], length=EMA_MEDIUM)
        df['EMA_200'] = ta.ema(df['close'], length=EMA_SLOW)

        # RSI
        df['RSI'] = ta.rsi(df['close'], length=RSI_PERIOD)

        # MACD
        macd = ta.macd(df['close'], fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL)
        if macd is not None and not macd.empty:
            df = df.join(macd)
            df.rename(columns={
                f'MACD_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD',
                f'MACDh_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD_hist',
                f'MACDs_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD_signal'
            }, inplace=True)

        # ATR
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=ATR_PERIOD)

        # ADX
        adx = ta.adx(df['high'], df['low'], df['close'], length=ADX_PERIOD)
        if adx is not None and not adx.empty:
            df = df.join(adx)
            df.rename(columns={
                f'ADX_{ADX_PERIOD}': 'ADX',
                f'DMP_{ADX_PERIOD}': 'DI_plus',
                f'DMN_{ADX_PERIOD}': 'DI_minus'
            }, inplace=True)

        # Bollinger Bands
        bb = ta.bbands(df['close'], length=BOLLINGER_PERIOD, std=BOLLINGER_STD_DEV)
        if bb is not None and not bb.empty:
            df = df.join(bb)
            df.rename(columns={
            f'BBL_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_lower',
            f'BBM_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_middle',
            f'BBU_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_upper',
            f'BBB_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_bandwidth',
            f'BBP_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_percent'
        }, inplace=True)

        # Donchian Channel
        dc = ta.donchian(df['high'], df['low'], lower_length=DONCHIAN_PERIOD, upper_length=DONCHIAN_PERIOD)
        if dc is not None and not dc.empty:
            df = df.join(dc)
            df.rename(columns={
                f'DCL_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_lower',
                f'DCM_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_middle',
                f'DCU_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_upper'
            }, inplace=True)

        # VWAP (Usually anchored to session/day)
        # We can approximate by computing standard VWAP if tick volume is used, but pandas_ta handles it with the vwap func
        # Often VWAP needs an anchor. pandas_ta.vwap defaults to session ('D') anchor if freq isn't specified perfectly
        try:
            vwap = ta.vwap(df['high'], df['low'], df['close'], df['tick_volume'])
            if vwap is not None:
                df['VWAP'] = vwap
        except Exception as e:
            logger.warning(f"Could not calculate VWAP: {e}")
            df['VWAP'] = np.nan

        return df

    def get_market_data(self, symbol, timeframe=TIMEFRAME, num_candles=500):
        """Fetch data and compute indicators returning a fully prepared DataFrame."""
        df = self.fetch_data(symbol, timeframe, num_candles)
        if df is not None:
            df = self.compute_indicators(df)
        return df

    def get_current_spread(self, symbol):
        """Get the current spread for a symbol."""
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return None
        return symbol_info.spread
