import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime, timedelta
from config import ANALYTICS_DIR

logger = logging.getLogger(__name__)

class PerformanceTracker:
    def __init__(self, magic_number=100100):
        self.magic_number = magic_number
        self.history_file = os.path.join(ANALYTICS_DIR, "performance_metrics.csv")
        self.trades_file = os.path.join(ANALYTICS_DIR, "trades_history.csv")

    def fetch_historical_trades(self, days_back=30) -> pd.DataFrame:
        """Fetch historical trades for the bot's magic number."""
        now = datetime.now()
        start = now - timedelta(days=days_back)
        
        history = mt5.history_deals_get(start, now)
        if history is None or len(history) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(list(history), columns=history[0]._asdict().keys())
        # Filter for our bot (magic == 100100) and actual trades (ENTRY_OUT or ENTRY_INOUT, meaning closed positions)
        df = df[df['magic'] == self.magic_number]
        df = df[df['entry'] == mt5.DEAL_ENTRY_OUT]
        
        if len(df) > 0:
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)

        return df

    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        """Calculates performance metrics from trades."""
        if df.empty:
            return {}

        total_trades = len(df)
        winning_trades = df[df['profit'] > 0]
        losing_trades = df[df['profit'] < 0]

        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        gross_profit = winning_trades['profit'].sum()
        gross_loss = abs(losing_trades['profit'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        df['equity_curve'] = df['profit'].cumsum()
        peak = df['equity_curve'].expanding(min_periods=1).max()
        drawdown = (df['equity_curve'] - peak)
        max_drawdown = drawdown.min()

        # Sharpe ratio approximation (assuming daily returns over trade returns)
        returns = df['profit']
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(total_trades) if returns.std() > 0 else 0

        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'net_profit': df['profit'].sum()
        }

    def update_analytics(self) -> dict:
        """Updates and saves analytics to CSV."""
        df = self.fetch_historical_trades()
        
        if df.empty:
            logger.info("No trades to analyze yet.")
            return {}

        # Save raw trades for AI filter training
        df.to_csv(self.trades_file)

        metrics = self.calculate_metrics(df)
        
        # Save metrics
        metrics_df = pd.DataFrame([metrics])
        if os.path.exists(self.history_file):
            metrics_df.to_csv(self.history_file, mode='a', header=False, index=False)
        else:
            metrics_df.to_csv(self.history_file, index=False)

        logger.info(f"Analytics updated: Win Rate {metrics['win_rate']*100:.1f}%, PF {metrics['profit_factor']:.2f}")
        return metrics
