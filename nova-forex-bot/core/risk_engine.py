import json

class RiskEngine:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.max_spread = 0.5 # Default max spread in pips for HFT
        self.max_latency_ms = 5.0

    def calculate_lot_size(self, balance, prob=None):
        """
        Calculates lot size dynamically based on AI confidence (Pseudo-Kelly criterion).
        """
        base_lot = self.config['trading']['lot_size'] # Base conservative lot
        
        if prob is not None:
            if prob >= 0.95:
                return round(base_lot * 3.0, 2) # Triple load on ultra-high edge
            elif prob >= 0.85:
                return round(base_lot * 2.0, 2) # Double load on very high edge
                
        return base_lot

    def check_kill_switches(self, symbol_info, ping_ms):
        """
        Safety check: Pause trading if spread or latency spike.
        """
        # Convert spread from points to pips
        spread_pips = symbol_info['spread'] / 10 
        
        if spread_pips > self.max_spread:
            print(f"KILL-SWITCH: Spread too wide ({spread_pips} pips)")
            return False
            
        if ping_ms > self.max_latency_ms:
            print(f"KILL-SWITCH: Latency too high ({ping_ms} ms)")
            return False
            
        return True

    def get_order_params(self, symbol, type, bid, ask):
        """
        Prepares order dictionary with HARD break-stops.
        """
        sl_delta = self.config['risk_management']['stop_loss_pips'] * 0.0001
        tp_delta = self.config['risk_management']['take_profit_pips'] * 0.0001
        
        if type == 'buy':
            price = ask
            sl = price - sl_delta
            tp = price + tp_delta
        else:
            price = bid
            sl = price + sl_delta
            tp = price - tp_delta
            
        return {
            "price": price,
            "sl": sl,
            "tp": tp
        }
