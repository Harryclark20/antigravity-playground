import json

class RiskEngine:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.max_spread = self.config['risk_management'].get('max_spread_pips', 0.5)
        self.max_latency_ms = self.config['risk_management'].get('max_latency_ms', 5.0)

    def calculate_lot_size(self, balance, prob=None):
        """
        Calculates lot size dynamically using the Half-Kelly fractional multiplier
        based on AI confidence and the configured precision Risk:Reward curve.
        """
        base_lot = self.config['trading']['lot_size'] # Base conservative lot
        
        if prob is None or prob <= 0.0:
            return base_lot
            
        tp = float(self.config['risk_management']['take_profit_pips'])
        sl = float(self.config['risk_management']['stop_loss_pips'])
        
        # Prevent division by zero during misconfiguration
        if sl <= 0 or tp <= 0:
            return base_lot
            
        r_ratio = tp / sl
        
        # Core Kelly Formula: W - ((1 - W) / R)
        kelly_fraction = prob - ((1.0 - prob) / r_ratio)
        
        if kelly_fraction <= 0:
            return base_lot
            
        # Apply Half-Kelly safety factor
        half_kelly = kelly_fraction * 0.5
        
        # Map to a dynamic multiplier curve (Max Cap = 5.0x Base Lot)
        lot_multiplier = 1.0 + (half_kelly * 5.0)
        lot_multiplier = min(lot_multiplier, 5.0)
        
        return round(base_lot * lot_multiplier, 2)

    def check_kill_switches(self, symbol_info, ping_ms, max_latency_override=None):
        """
        Safety check: Pause trading if spread or latency spike.
        """
        # Convert spread from points to pips
        spread_pips = symbol_info['spread'] / 10 
        
        if spread_pips > self.max_spread:
            print(f"KILL-SWITCH: Spread too wide ({spread_pips} pips)")
            return False
            
        limit = max_latency_override if max_latency_override is not None else self.max_latency_ms
        if ping_ms > limit:
            print(f"KILL-SWITCH: Latency too high ({ping_ms} ms)")
            return False
            
        return True

    def get_order_params(self, symbol, type, bid, ask, volatility):
        """
        Prepares order dictionary with DYNAMIC Volatility-based barriers.
        TP = 3.0 * Standard Deviation
        SL = 2.0 * Standard Deviation
        """
        # Minimum barrier to prevent tiny targets (0.2 pips)
        min_barrier = 0.00002 
        
        tp_dist = max(volatility * 3.0, min_barrier)
        sl_dist = max(volatility * 2.0, min_barrier)
        
        if type == 'buy':
            price = ask
            sl = price - sl_dist
            tp = price + tp_dist
        else:
            price = bid
            sl = price + sl_dist
            tp = price - tp_dist
            
        return {
            "price": price,
            "sl": sl,
            "tp": tp
        }
