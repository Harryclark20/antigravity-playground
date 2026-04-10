import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime
from data_engine import DataEngine
from sniper import SniperStrategy
from risk_manager import RiskManager

from master_overseer import MasterOverseer

class LiveTrader:
    def __init__(self, symbol="EURUSD"):
        print(f"--- APEX TRI-CORE MASTER TRADER INITIALIZING [{symbol}] ---")
        self.symbol = symbol
        self.engine = DataEngine()
        
        # 1. The Sniper Core (M5)
        self.sniper_strategy = SniperStrategy()
        
        # 2. The Trend/Range Core (H1)
        self.master_overseer = MasterOverseer(adx_threshold=25)
        
        # 3. Dynamic Risk Manager (High Leverage for "Massive Returns")
        self.risk_mgr = RiskManager(risk_percent=0.05)
        
        # 4. Trailing Stop Thresholds
        self.trailing_activation_pips = 4.0   # Start trailing when 4 pips in profit
        self.trailing_distance_pips = 2.0     # Trail just 2 pips behind price
        
        # Verify symbol exists and is visible in Market Watch
        if not mt5.symbol_select(self.symbol, True):
             print(f"Failed to select {self.symbol}. Exiting.")
             mt5.shutdown()
             quit()

    def _get_current_position(self):
        """Checks if there is already an open position for this symbol."""
        positions = mt5.positions_get(symbol=self.symbol)
        if positions is None:
             print("Error checking positions, error code =", mt5.last_error())
             return None
        return positions[0] if len(positions) > 0 else None

    def _place_order(self, order_type, price, sl, tp, volume):
        """Sends an exact execution order to the MetaTrader 5 broker server."""
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20, # Slippage tolerance
            "magic": 234000, # Bot ID
            "comment": "Apex Sniper Autotrade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send a trading request
        print(f"Sending Order: {request}")
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order send failed, retcode =", result.retcode)
            return False
            
        print(f"Order Successfully Placed! Ticket: {result.order}")
        return True

    def calculate_trade_params(self, direction, price, atr):
         # Risk:Reward parameters tuned for the 80% Win Rate Setup
         sl_multiplier = 2.0 
         tp_multiplier = 0.5
         
         if direction == 'LONG':
             sl = price - (atr * sl_multiplier)
             tp = price + (atr * tp_multiplier)
         else:
             sl = price + (atr * sl_multiplier)
             tp = price - (atr * tp_multiplier)
             
         sl_pips = abs(price - sl)
         volume = self.risk_mgr.calculate_lot_size(self.symbol, sl_pips)
         
         return sl, tp, volume

    def _manage_trailing_stops(self):
        """Scans open positions and moves stop losses to Break-Even or Trails them to lock in profit."""
        position = self._get_current_position()
        if not position: return
        
        symbol_info = mt5.symbol_info(self.symbol)
        
        # Convert pip thresholds to raw price ticks
        activation_dist = self.trailing_activation_pips * symbol_info.trade_tick_size * 10 
        trail_dist = self.trailing_distance_pips * symbol_info.trade_tick_size * 10
        
        new_sl = position.sl
        modify = False
        
        # LONG Position Trailing
        if position.type == mt5.ORDER_TYPE_BUY:
            current_profit_dist = symbol_info.bid - position.price_open
            
            # If profit > activation threshold AND the new calculated SL is better than the current SL
            if current_profit_dist > activation_dist:
                 potential_sl = symbol_info.bid - trail_dist
                 if potential_sl > position.sl:
                      new_sl = potential_sl
                      modify = True
                      
        # SHORT Position Trailing
        elif position.type == mt5.ORDER_TYPE_SELL:
             current_profit_dist = position.price_open - symbol_info.ask
             
             if current_profit_dist > activation_dist:
                  potential_sl = symbol_info.ask + trail_dist
                  if potential_sl < position.sl or position.sl == 0:
                       new_sl = potential_sl
                       modify = True
                       
        if modify:
             request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": position.ticket,
                "symbol": self.symbol,
                "sl": new_sl,
                "tp": position.tp,
                "magic": 234000
             }
             mt5.order_send(request)
             print(f">>> Trailing Stop tightened to {new_sl} to minimize loss! <<<")

    def run_tick_cycle(self):
        """The core loop executed every few seconds to check for multi-timeframe setups."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Awaiting Setup...")
        
        # 1. Manage existing positions with hyper-aggressive trailing stops
        if self._get_current_position() is not None:
             self._manage_trailing_stops()
             return
             
        # ==========================================
        # CORE 1: THE SNIPER SCALPER (M5)
        # ==========================================
        df_m5_raw = self.engine.fetch_historical_data(self.symbol, mt5.TIMEFRAME_M5, num_candles=50)
        if df_m5_raw is not None:
            df_m5_indicators = self.sniper_strategy.calculate_snip_indicators(df_m5_raw)
            df_m5_signals = self.sniper_strategy.generate_signals(df_m5_indicators)
            
            latest_m5_signal = df_m5_signals.iloc[-1]['signal']
            latest_m5_atr = df_m5_signals.iloc[-1]['atr_5']
            
            if latest_m5_signal != 0:
                 self._execute_trade(latest_m5_signal, latest_m5_atr, 'Sniper')
                 return # Exit cycle if trade placed to avoid double execution

        # ==========================================
        # CORES 2 & 3: TREND FOLLOWING & MEAN REVERSION (H1)
        # ==========================================
        df_h1_raw = self.engine.fetch_historical_data(self.symbol, mt5.TIMEFRAME_H1, num_candles=250)
        if df_h1_raw is not None:
             master_setup = self.master_overseer.calculate_master_indicators(df_h1_raw)
             master_signals = self.master_overseer.generate_routed_signals(master_setup)
             
             latest_h1_signal = master_signals.iloc[-1]['master_signal']
             latest_h1_atr = master_signals.iloc[-1]['atr_14']
             regime = master_signals.iloc[-1]['regime']
             
             if latest_h1_signal != 0:
                  print(f"*** {regime} SETUP DETECTED ***")
                  self._execute_trade(latest_h1_signal, latest_h1_atr, 'Swing')

    def _execute_trade(self, signal_dir, trigger_atr, source):
         symbol_info = mt5.symbol_info(self.symbol)
         if signal_dir == 1:
              ask_price = symbol_info.ask
              print(f"*** [{source}] BUY SIGNAL DETECTED AT {ask_price:.5f} ***")
              sl, tp, volume = self.calculate_trade_params('LONG', ask_price, trigger_atr)
              self._place_order(mt5.ORDER_TYPE_BUY, ask_price, sl, tp, volume)
         elif signal_dir == -1:
              bid_price = symbol_info.bid
              print(f"*** [{source}] SELL SIGNAL DETECTED AT {bid_price:.5f} ***")
              sl, tp, volume = self.calculate_trade_params('SHORT', bid_price, trigger_atr)
              self._place_order(mt5.ORDER_TYPE_SELL, bid_price, sl, tp, volume)

    def start(self):
         """Starts the infinite execution loop."""
         print("Live Execution Engine Started. Press Ctrl+C to Stop.")
         try:
             while True:
                 self.run_tick_cycle()
                 # Sleep for 10 seconds to avoid spamming the MT5 terminal API
                 time.sleep(10) 
         except KeyboardInterrupt:
             print("\nBot halted by user.")
             self.engine.shutdown()

if __name__ == "__main__":
    bot = LiveTrader("EURUSD")
    bot.start()
