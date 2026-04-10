class RiskManager:
    def __init__(self, account_balance=10000.0, risk_per_trade_pct=0.01):
        self.initial_balance = account_balance
        self.account_balance = account_balance
        self.risk_per_trade_pct = risk_per_trade_pct
        
    def calculate_position_size(self, entry_price, stop_loss):
        if entry_price == stop_loss:
            return 0
        risk_amount = self.account_balance * self.risk_per_trade_pct
        risk_per_unit = abs(entry_price - stop_loss)
        return risk_amount / risk_per_unit
        
    def validate_risk_reward(self, entry_price, stop_loss, take_profit, min_rr=1.5):
        # Ensure we have a structural edge (Wins outshine losses)
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        if risk == 0:
            return False
            
        rr_ratio = reward / risk
        return rr_ratio >= min_rr
        
    def update_balance(self, pnl):
        self.account_balance += pnl
        
    def get_drawdown(self):
        return (self.initial_balance - self.account_balance) / self.initial_balance if self.account_balance < self.initial_balance else 0.0
