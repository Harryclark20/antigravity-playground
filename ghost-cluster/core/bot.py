import pandas as pd
from core.risk_manager import RiskManager

class Bot:
    def __init__(self, data_feed, strategy_manager, initial_balance=10000.0):
        self.data_feed = data_feed
        self.strategy_manager = strategy_manager
        self.risk_manager = RiskManager(account_balance=initial_balance)
        self.history = pd.DataFrame()
        self.trades = []
        self.open_position = None

    def execute_trade(self, signal, bar_index, current_price):
        if not self.risk_manager.validate_risk_reward(signal['entry'], signal['sl'], signal['tp'], min_rr=1.5):
            return

        size = self.risk_manager.calculate_position_size(signal['entry'], signal['sl'])
        if size <= 0: return

        self.open_position = {
            'action': signal['action'],
            'entry': signal['entry'],
            'sl': signal['sl'],
            'tp': signal['tp'],
            'size': size,
            'entry_time': bar_index
        }

    def close_position(self, exit_price, exit_time, reason):
        if not self.open_position: return
        
        pos = self.open_position
        if pos['action'] == 'BUY':
            pnl = (exit_price - pos['entry']) * pos['size']
        else:
            pnl = (pos['entry'] - exit_price) * pos['size']
            
        self.risk_manager.update_balance(pnl)
        
        # Determine if it was actually a win or loss based on PNL
        # Even if SL was hit, if we moved SL to breakeven, it's not a loss
        actual_reason = reason
        if pnl > 0 and reason == 'SL':
            actual_reason = 'BREAK_EVEN/TRAILING'
            
        self.trades.append({
            'entry_time': pos['entry_time'],
            'exit_time': exit_time,
            'action': pos['action'],
            'entry_price': pos['entry'],
            'exit_price': exit_price,
            'pnl': pnl,
            'reason': actual_reason
        })
        self.open_position = None

    def run_simulation(self):
        df = self.data_feed.get_data()
        self.history = df.copy()
        
        self.strategy_manager.prepare_data(self.history)
        
        for index, row in self.history.iterrows():
            current_price = row['Close']
            
            if self.open_position:
                pos = self.open_position
                dist_to_tp = abs(pos['tp'] - pos['entry'])
                
                if pos['action'] == 'BUY':
                    dist_moved = row['High'] - pos['entry']
                    # Sensible Break-Even logic: Move SL to entry + 5% of TP once 50% to TP
                    if dist_moved >= dist_to_tp * 0.5:
                        pos['sl'] = max(pos['sl'], pos['entry'] + (dist_to_tp * 0.05))

                    if row['Low'] <= pos['sl']:
                        self.close_position(pos['sl'], index, 'SL')
                    elif row['High'] >= pos['tp']:
                        self.close_position(pos['tp'], index, 'TP')

                else: # SELL
                    dist_moved = pos['entry'] - row['Low']
                    if dist_moved >= dist_to_tp * 0.5:
                        pos['sl'] = min(pos['sl'], pos['entry'] - (dist_to_tp * 0.05))
                        
                    if row['High'] >= pos['sl']:
                        self.close_position(pos['sl'], index, 'SL')
                    elif row['Low'] <= pos['tp']:
                        self.close_position(pos['tp'], index, 'TP')
                continue 
            
            signal = self.strategy_manager.evaluate(index, row, self.history)
            if signal['action'] != 'HOLD':
                self.execute_trade(signal, index, current_price)

        return self.trades, self.risk_manager.account_balance
