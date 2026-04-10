import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Backtester:
    def __init__(self, df, initial_balance=10000.0, risk_per_trade=0.01, break_even_pips=7.0):
        """
        Initializes the Backtester with a simulated account.
        
        Args:
            df (pd.DataFrame): DataFrame containing OHLCV data, indicators, signals.
            initial_balance (float): Starting account balance in base currency.
            risk_per_trade (float): Percentage of account equity risked per trade (e.g., 0.01 for 1%).
            break_even_pips (float): Move SL to entry if price moves this many pips in favor.
        """
        self.df = df
        self.balance = initial_balance
        self.equity = initial_balance
        self.risk_per_trade = risk_per_trade
        self.break_even_pips = break_even_pips
        self.trades = []
        self.in_position = False
        self.position = None  # None, 'LONG', 'SHORT'
        self.entry_price = 0.0
        self.stop_loss = 0.0
        self.take_profit = 0.0
        self.lot_size = 0.0

    def calculate_lot_size(self, stop_loss_pips):
        """
        Calculates position size based on risking x% of the current equity.
        Assuming standard Forex lots (1 lot = 100,000 units).
        """
        risk_amount = self.equity * self.risk_per_trade
        # Assuming EURUSD or similar where pip value is approx $10 per standard lot
        # Simplification for backtesting purposes. Actual MT5 uses symbols info.
        pip_value_per_lot = 10.0 
        
        # Avoid division by zero if ATR drops to extremely low values
        if stop_loss_pips <= 0:
            stop_loss_pips = 1.0  
            
        lots = risk_amount / (stop_loss_pips * pip_value_per_lot)
        return round(lots, 2)

    def run(self):
        """Executes the backtest loop across the historical dataframe."""
        dates = self.df.index
        closes = self.df['close'].values
        highs = self.df['high'].values
        lows = self.df['low'].values
        signals = self.df.get('signal', pd.Series([0]*len(self.df))).values
        atrs = self.df['atr'].values
        
        for i in range(1, len(self.df)):
            curr_date = dates[i]
            curr_close = closes[i]
            curr_high = highs[i]
            curr_low = lows[i]
            curr_signal = signals[i]
            curr_atr = atrs[i]

            # 1. Check for Exits (Stop Loss / Take Profit hits, and Break-Even trailing)
            if self.in_position:
                if self.position == 'LONG':
                    # Check break-even trigger
                    if (curr_high - self.entry_price) * 10000 >= self.break_even_pips and self.stop_loss < self.entry_price:
                         self.stop_loss = self.entry_price # Move SL to entry

                    if curr_low <= self.stop_loss:
                        # Stop Loss hit
                        self._close_position(curr_date, self.stop_loss, 'StopLoss/BE')
                    elif curr_high >= self.take_profit:
                        # Take Profit hit
                        self._close_position(curr_date, self.take_profit, 'TakeProfit')

                elif self.position == 'SHORT':
                    # Check break-even trigger
                    if (self.entry_price - curr_low) * 10000 >= self.break_even_pips and self.stop_loss > self.entry_price:
                         self.stop_loss = self.entry_price # Move SL to entry

                    if curr_high >= self.stop_loss:
                         # Stop Loss hit
                         self._close_position(curr_date, self.stop_loss, 'StopLoss/BE')
                    elif curr_low <= self.take_profit:
                         # Take Profit hit
                         self._close_position(curr_date, self.take_profit, 'TakeProfit')

            # 2. Check for Entries
            if not self.in_position:
                if curr_signal == 1: # BUY
                    params = self._calculate_trade_params('LONG', curr_close, curr_atr)
                    self._open_position(curr_date, 'LONG', params['entry'], params['sl'], params['tp'], params['lots'])
                
                elif curr_signal == -1: # SELL
                    params = self._calculate_trade_params('SHORT', curr_close, curr_atr)
                    self._open_position(curr_date, 'SHORT', params['entry'], params['sl'], params['tp'], params['lots'])

    def _calculate_trade_params(self, direction, price, atr):
        """Calculates dynamic SL and TP based on ATR volatility."""
        # For a high-probability scalper (80%+ WR), we need a wider SL to avoid noise,
        # and a very tight TP to quickly secure profits.
        sl_multiplier = 2.0 
        tp_multiplier = 0.5
        
        if direction == 'LONG':
            sl = price - (atr * sl_multiplier)
            tp = price + (atr * tp_multiplier)
        else:
            sl = price + (atr * sl_multiplier)
            tp = price - (atr * tp_multiplier)
            
        sl_pips = abs(price - sl) * 10000 # Convert raw difference to standard pips
        lots = self.calculate_lot_size(sl_pips)
        
        return {'entry': price, 'sl': sl, 'tp': tp, 'lots': lots}

    def _open_position(self, date, side, price, sl, tp, lots):
        self.in_position = True
        self.position = side
        self.entry_price = price
        self.stop_loss = sl
        self.take_profit = tp
        self.lot_size = lots
        
        # print(f"[{date}] OPEN {side} @ {price:.4f} (SL: {sl:.4f}, TP: {tp:.4f})")

    def _close_position(self, date, price, reason):
        # Calculate PnL
        point_diff = (price - self.entry_price) if self.position == 'LONG' else (self.entry_price - price)
        pip_diff = point_diff * 10000
        pnl = pip_diff * 10.0 * self.lot_size # Simplified pip value calculation
        
        self.equity += pnl
        
        trade_record = {
            'Close Date': date,
            'Side': self.position,
            'Entry Price': self.entry_price,
            'Exit Price': price,
            'Reason': reason,
            'PnL': pnl,
            'Equity': self.equity
        }
        self.trades.append(trade_record)
        
        self.in_position = False
        self.position = None

    def print_performance(self):
        """Calculates and displays core algorithmic performance metrics."""
        if not self.trades:
            print("\n--- PERFORMANCE SUMMARY ---")
            print("Zero trades were taken.")
            return
            
        trades_df = pd.DataFrame(self.trades)
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['PnL'] > 0])
        losing_trades = len(trades_df[trades_df['PnL'] <= 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
        gross_loss = abs(trades_df[trades_df['PnL'] <= 0]['PnL'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        net_profit = sum(t['PnL'] for t in self.trades)
        return_pct = (net_profit / self.balance) * 100
        
        print("\n--- PERFORMANCE SUMMARY ---")
        print(f"Total Trades Taken: {total_trades}")
        print(f"Win Rate:           {win_rate:.2f}% ({winning_trades} W / {losing_trades} L)")
        print(f"Return on Account:  {return_pct:.2f}% (Starting: ${self.balance}, Ending: ${self.balance + net_profit:.2f})")
        print(f"Profit Factor:      {profit_factor:.2f}")

        # Plot equity curve
        trades_df.set_index('Close Date', inplace=True)
        trades_df['Equity'].plot(title="Backtest Equity Curve", figsize=(10,5))
        plt.xlabel("Date Axis")
        plt.ylabel("Account Balance ($)")
        plt.grid()
        plt.savefig("backtest_equity_curve.png")
        print("\nEquity curve chart saved as 'backtest_equity_curve.png'")
        
        # Save exact trades list for manual verification
        trades_df.to_csv("backtest_trades_log.csv")
        print("Detailed trade log saved as 'backtest_trades_log.csv'")
