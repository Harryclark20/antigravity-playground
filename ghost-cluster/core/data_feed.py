import yfinance as yf
import pandas as pd
import datetime

class DataFeed:
    def __init__(self, symbol='EURUSD=X', interval='1h', days_back=60):
        self.symbol = symbol
        self.interval = interval
        self.days_back = days_back
        self.data = pd.DataFrame()

    def fetch_data(self, silent=False):
        if not silent:
            print(f"[*] Fetching {self.days_back} days of {self.interval} data for {self.symbol}...")
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days_back)
        
        # yfinance allows 60 days max for 1h or 15m intervals usually
        df = yf.download(self.symbol, start=start_date, end=end_date, interval=self.interval, progress=False)
        
        # Flatten MultiIndex columns if yfinance returns them
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
            
        df.dropna(inplace=True)
        self.data = df
        if not silent:
            print(f"[*] Fetched {len(self.data)} candles.")
        return self.data

    def get_data(self):
        return self.data
