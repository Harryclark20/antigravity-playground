import MetaTrader5 as mt5

class RiskManager:
    def __init__(self, risk_percent=0.05):
        """
        Calculates position sizes to ensure strict risk management.
        
        Args:
            risk_percent (float): The percentage of account equity to risk per trade.
                                  Set to 5% (0.05) for high-yield, aggressive scalping.
        """
        self.risk_percent = risk_percent

    def calculate_lot_size(self, symbol, sl_pips):
        """
        Calculates the exact lot size for a trade based on the account balance,
        the currency pair's tick value, and the distance to the stop loss.
        """
        account_info = mt5.account_info()
        if account_info is None:
            print("Failed to get account info.")
            return 0.0
            
        equity = account_info.equity
        risk_amount = equity * self.risk_percent
        
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"Failed to get symbol info for {symbol}.")
            return 0.0
            
        # Get the value of one pip in the account's base currency
        # This handles cross pairs (like GBPJPY on a USD account) automatically via MT5
        tick_value = symbol_info.trade_tick_value
        tick_size = symbol_info.trade_tick_size
        
        if tick_value == 0 or tick_size == 0 or sl_pips == 0:
            return 0.0
            
        # If sl_pips is in standard pips (0.0001 for EURUSD), 
        # we convert it to raw ticks based on the symbol's tick size
        sl_ticks = sl_pips / tick_size
        
        # Calculate volume
        volume = risk_amount / (sl_ticks * tick_value)
        
        # Normalize volume to broker constraints
        min_vol = symbol_info.volume_min
        max_vol = symbol_info.volume_max
        step_vol = symbol_info.volume_step
        
        # Round down to the nearest integer multiple of step_vol
        normalized_volume = (volume // step_vol) * step_vol
        
        # Enforce min/max broker constraints
        if normalized_volume < min_vol:
            normalized_volume = min_vol
            print(f"Warning: Calculated lot size was below broker minimum. Using {min_vol}.")
        elif normalized_volume > max_vol:
            normalized_volume = max_vol
            print(f"Warning: Calculated lot size exceeded broker maximum. Capped at {max_vol}.")
            
        return round(normalized_volume, 2)
