import logging

class RiskManager:
    def __init__(self, risk_percent, max_spread):
        self.risk_percent = risk_percent
        self.max_spread = max_spread
        
    def calculate_lot_size(self, balance, entry_price, sl_price, symbol_info):
        """
        Calculates position size in lots based on risk percentage.
        symbol_info should contain tick_value, trade_contract_size.
        """
        try:
            risk_amount = balance * (self.risk_percent / 100.0)
            sl_pips = abs(entry_price - sl_price) / symbol_info.point
            point_value = symbol_info.trade_tick_value
            
            if sl_pips == 0 or point_value == 0:
                return 0.01
                
            lot_size = risk_amount / (sl_pips * point_value)
            
            # Respect broker limits
            if lot_size < symbol_info.volume_min:
                lot_size = symbol_info.volume_min
            elif lot_size > symbol_info.volume_max:
                lot_size = symbol_info.volume_max
                
            volume_step = symbol_info.volume_step
            lot_size = round(lot_size / volume_step) * volume_step
            
            return round(lot_size, 2)
        except Exception as e:
            logging.error(f"Error calculating lot size: {e}")
            return 0.01
