import asyncio
import logging
import sys
import os
import time
from datetime import datetime

# Setup enhanced logging
logger = logging.getLogger('ForexBot')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

from config import (
    SYMBOLS, TIMEFRAME, 
    RISK_PER_TRADE_PERCENT, MAX_DAILY_LOSS_PERCENT,
    MAX_TRADES_PER_DAY, MAX_CONSECUTIVE_LOSSES,
    MIN_VOTES_REQUIRED, AI_PROBABILITY_THRESHOLD,
    MIN_SIGNAL_CONFIDENCE, MIN_RISK_REWARD_RATIO,
    LOGS_DIR
)

fh = logging.FileHandler(os.path.join(LOGS_DIR, "bot.log"))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

from data.engine import DataEngine
from strategies.regime_detector import RegimeDetector
from strategies.trend_pullback import TrendPullbackStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.liquidity_sweep import LiquiditySweepStrategy
from strategies.breakout_expansion import BreakoutExpansionStrategy
from strategies.session_momentum import SessionMomentumStrategy
from strategies.volatility_sniper import VolatilitySniperStrategy
from strategies.xau_volatility_breakout import PreciousMetalsVolatilityBreakoutStrategy
from strategies.voter import SignalVoter
from models.ai_filter import AIFilter
from execution.risk_manager import RiskManager
from execution.position_sizer import PositionSizer
from execution.order_manager import OrderManager
from execution.trade_manager import TradeManager
from analytics.performance import PerformanceTracker

class TradingAdvisor:
    def __init__(self):
        self.data_engine = DataEngine()
        
        # Engines
        self.regime_detector = RegimeDetector()
        self.strategies = {
            'trend': TrendPullbackStrategy(),
            'mean_rev': MeanReversionStrategy(),
            'liquidity': LiquiditySweepStrategy(),
            'breakout': BreakoutExpansionStrategy(),
            'momentum': SessionMomentumStrategy(),
            'sniper': VolatilitySniperStrategy(),
            'xau_breakout': PreciousMetalsVolatilityBreakoutStrategy()
        }
        self.voter = SignalVoter(min_votes=MIN_VOTES_REQUIRED)
        self.ai_filter = AIFilter(threshold=AI_PROBABILITY_THRESHOLD)
        
        self.risk_manager = RiskManager(
            max_daily_loss_percent=MAX_DAILY_LOSS_PERCENT,
            max_trades_per_day=MAX_TRADES_PER_DAY,
            max_consecutive_losses=MAX_CONSECUTIVE_LOSSES
        )
        self.position_sizer = PositionSizer(default_risk_percent=RISK_PER_TRADE_PERCENT)
        self.order_manager = OrderManager()
        self.trade_manager = TradeManager()
        self.performance = PerformanceTracker()

    async def initialize(self) -> bool:
        if not self.data_engine.connect():
            logger.critical("Failed to connect to MT5.")
            return False
            
        logger.info("Bot components initialized.")
        return True

    def _process_symbol(self, symbol: str):
        # 1. Fetch Data
        df = self.data_engine.get_market_data(symbol, timeframe=TIMEFRAME)
        if df is None or df.empty:
            return

        current_price = df.iloc[-1]['close']
        current_atr = df.iloc[-1].get('ATR', 0)

        # 2. Trade Management (Runs every tick regardless of signal)
        self.trade_manager.manage_positions(symbol, current_price, current_atr)

        # Evaluate signals only on new candles, or roughly every few seconds if needed
        # MT5 doesn't broadcast 'new bar' natively in python easily without tracking time
        # We will assume this loop takes a moment and run it iteratively
        # 3. Market Regime
        regime = self.regime_detector.detect(df)
        
        # 4. Strategy Generation
        results = {}
        # Simple regime filter logic example
        active_strategies = []
        if regime == "TREND":
            active_strategies = ['trend', 'breakout', 'momentum', 'xau_breakout']
        elif regime == "RANGE":
            active_strategies = ['mean_rev', 'liquidity']
        elif regime == "VOLATILE":
            active_strategies = ['sniper', 'breakout', 'mean_rev', 'xau_breakout']
        elif regime == "LOW VOLATILITY":
            active_strategies = ['sniper', 'breakout']
        else:
            active_strategies = list(self.strategies.keys())

        for name in active_strategies:
            strat = self.strategies[name]
            # Capture the feature state and result (includes weight if defined)
            results[name] = strat.analyze(df)

        # 5. Signal Voting System
        vote_result = self.voter.evaluate(results)
        final_signal = vote_result['signal']

        if final_signal == 'NO_TRADE':
            return
            
        vote_confidence = vote_result.get('confidence', 0.0)
        if vote_confidence < MIN_SIGNAL_CONFIDENCE:
            logger.info(f"{symbol} - Skipping trade: vote confidence too low ({vote_confidence:.2f})")
            return
            
        sl_distance = vote_result.get('sl_distance', 0.0)
        tp_distance = vote_result.get('tp_distance', 0.0)
        if sl_distance <= 0 or tp_distance <= 0:
            logger.info(f"{symbol} - Skipping trade: invalid risk distances sl={sl_distance} tp={tp_distance}")
            return

        rr_ratio = tp_distance / sl_distance if sl_distance > 0 else 0
        if rr_ratio < MIN_RISK_REWARD_RATIO:
            logger.info(f"{symbol} - Skipping trade: RR {rr_ratio:.2f} < {MIN_RISK_REWARD_RATIO}")
            return

        logger.info(f"{symbol} - Regime: {regime} - Signal: {final_signal} (Votes: {vote_result['votes']}, Confidence:{vote_confidence:.2f}, RR:{rr_ratio:.2f})")

        # 6. AI Probability Filter
        if not self.ai_filter.filter_signal(df, final_signal):
            return

        # 7. Risk Management Rules
        if not self.risk_manager.can_trade():
            logger.info("Trade blocked by Risk Manager.")
            return

        # 8. Execution Engine
        # Calculate sizing
        lot_size = self.position_sizer.calculate_lot_size(symbol, vote_result['sl_distance'])
        
        if lot_size <= 0:
            logger.info("Calculated lot size is 0. Aborting.")
            return

        # Execute
        sl_price = 0.0
        tp_price = 0.0
        
        if final_signal == 'BUY':
            sl_price = current_price - vote_result['sl_distance'] if vote_result['sl_distance'] > 0 else 0
            tp_price = current_price + vote_result['tp_distance'] if vote_result.get('tp_distance') else 0
        else:
            sl_price = current_price + vote_result['sl_distance'] if vote_result['sl_distance'] > 0 else 0
            tp_price = current_price - vote_result['tp_distance'] if vote_result.get('tp_distance') else 0

        # Optional: Some strategies return explicit sl_price or tp_price instead of distance.
        result = self.order_manager.execute_trade(symbol, final_signal, lot_size, sl_price, tp_price)
        
        if result['success']:
            self.risk_manager.record_trade_start()

    async def run(self):
        if not await self.initialize():
            return
            
        logger.info(f"Starting Elite Hybrid Autonomous Trading loop on: {SYMBOLS}")
        last_analytics_update = time.time()
        
        try:
            while True:
                for symbol in SYMBOLS:
                    try:
                        self._process_symbol(symbol)
                    except Exception as e:
                        logger.error(f"Error processing {symbol}: {e}")
                
                # Update analytics every hour
                if time.time() - last_analytics_update > 3600:
                    self.performance.update_analytics()
                    last_analytics_update = time.time()
                    
                # Small sleep to prevent CPU overload
                await asyncio.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Bot shutting down...")
        finally:
            self.data_engine.disconnect()


if __name__ == "__main__":
    bot = TradingAdvisor()
    asyncio.run(bot.run())
