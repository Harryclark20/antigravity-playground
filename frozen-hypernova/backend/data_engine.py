import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz

class DataEngine:
    def __init__(self):
        """Initializes connection to MT5 terminal."""
        # Establish connection to the MetaTrader 5 terminal
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()
        else:
            print("MetaTrader5 initialized successfully.")

    def fetch_historical_data(self, symbol, timeframe, num_candles, start_pos=0):
        """
        Fetches historical candlestick data for a given symbol.
        
        Args:
            symbol (str): The currency pair (e.g., 'EURUSD').
            timeframe: MT5 timeframe constant (e.g., mt5.TIMEFRAME_H1).
            num_candles (int): Number of historical bars to retrieve.
            start_pos (int): Starting index from the current time.
            
        Returns:
            pd.DataFrame: A Pandas DataFrame containing OHLCV data.
        """
        print(f"Fetching {num_candles} candles for {symbol} on {(timeframe)}...")
        rates = mt5.copy_rates_from_pos(symbol, timeframe, start_pos, num_candles)
        
        if rates is None or len(rates) == 0:
            print(f"Failed to fetch data for {symbol}, error code =", mt5.last_error())
            return None

        # Create DataFrame out of the obtained data
        df = pd.DataFrame(rates)
        
        # Convert time in seconds into the datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Set time as index
        df.set_index('time', inplace=True)
        
        # Rename 'tick_volume' to simply 'volume'
        if 'tick_volume' in df.columns:
            df.rename(columns={'tick_volume': 'volume'}, inplace=True)
            
        return df

    def shutdown(self):
        """Closes connection to the MT5 terminal."""
        mt5.shutdown()
        print("MetaTrader5 connection closed.")

# Usage example
if __name__ == "__main__":
    engine = DataEngine()
    # Fetch 500 hours of EURUSD data
    df = engine.fetch_historical_data("EURUSD", mt5.TIMEFRAME_H1, 500)
    if df is not None:
        print(df.head())
    engine.shutdown()
