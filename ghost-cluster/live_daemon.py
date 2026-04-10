import time
import datetime
import pandas as pd
from core.data_feed import DataFeed
from strategies.strategy_manager import StrategyManager
from strategies.mean_reversion import MeanReversionStrategy
from strategies.ict_momentum import ICTMomentumStrategy

# Optional: MetaTrader 5 Integration
# pip install MetaTrader5
try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

ENABLE_LIVE_EXECUTION = True # Set this to True when you want to execute real/demo trades
MT5_LOGIN = 5047825822 # Replace with your MT5 account ID
MT5_PASSWORD = "RpUaG_K5" # Replace with your MT5 password
MT5_SERVER = "MetaQuotes-Demo" # Replace with your broker server string

class LiveTradingDaemon:
    def __init__(self, pairs, interval='1h'):
        self.pairs = pairs
        self.interval = interval
        self.manager = StrategyManager()
        self.manager.add_strategy('mean_reversion', MeanReversionStrategy())
        self.manager.add_strategy('momentum', ICTMomentumStrategy())
        
        self.open_positions = {pair: None for pair in pairs}
        
    def _execute_mt5_trade(self, action, pair, sl, tp, volume=0.1):
        if not MT5_AVAILABLE or not ENABLE_LIVE_EXECUTION:
            return
            
        # Format symbol for MT5 mapping (e.g., 'GBPJPY=X' -> 'GBPJPY')
        symbol = pair.replace('=X', '').replace('-', '') 
        
        order_type = mt5.ORDER_TYPE_BUY if action == 'BUY' else mt5.ORDER_TYPE_SELL
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "sl": float(sl),
            "tp": float(tp),
            "deviation": 20,
            "magic": 999999,
            "comment": "Antigravity Autonomous Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        print(f"  [MT5 API] Sending {action} order for {symbol}...")
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"  [ERROR] MT5 Order failed: {result.retcode}")
        else:
            print(f"  [SUCCESS] MT5 Executed Ticket: {result.order}")

    def poll_market(self):
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Polling Core Market Pairs...")
        
        for pair in self.pairs:
            feed = DataFeed(symbol=pair, interval=self.interval, days_back=10)
            df = feed.fetch_data(silent=True)
            if df.empty:
                print(f"  [!] Failed to pull latest data for {pair}.")
                continue
                
            self.manager.prepare_data(df)
            last_index = df.index[-2]
            last_row = df.iloc[-2]
            current_price = df.iloc[-1]['Close'] 
            
            pos = self.open_positions[pair]
            if pos:
                print(f"  [INFO] {pair} Holding active {pos['action']} position from {pos['entry']:.5f} (Current: {current_price:.5f}).")
                if pos['action'] == 'BUY':
                    if current_price <= pos['sl']:
                        print(f"  --> [!] {pair} STOP LOSS HIT at {current_price:.5f}. Reason: Market reversed.")
                        self.open_positions[pair] = None
                    elif current_price >= pos['tp']:
                        print(f"  --> [$$] {pair} TAKE PROFIT HIT at {current_price:.5f}. Reason: Reached Target.")
                        self.open_positions[pair] = None
                else: 
                    if current_price >= pos['sl']:
                        print(f"  --> [!] {pair} STOP LOSS HIT at {current_price:.5f}. Reason: Market reversed.")
                        self.open_positions[pair] = None
                    elif current_price <= pos['tp']:
                        print(f"  --> [$$] {pair} TAKE PROFIT HIT at {current_price:.5f}. Reason: Reached Target.")
                        self.open_positions[pair] = None
                continue 
                
            signal = self.manager.evaluate(last_index, last_row, df)
            
            if signal['action'] != 'HOLD':
                print(f"  [EXECUTIVE SIGNAL] ---> {signal['action']} {pair} at {current_price:.5f} "
                      f"(SL: {signal['sl']:.5f}, TP: {signal['tp']:.5f})")
                
                # Trigger live MT5 execution
                self._execute_mt5_trade(signal['action'], pair, signal['sl'], signal['tp'])

                self.open_positions[pair] = {
                    'action': signal['action'],
                    'entry': current_price,
                    'sl': signal['sl'],
                    'tp': signal['tp']
                }
            else:
                print(f"  [INFO] No edge detected on {pair}. Holding capital.")

    def start(self, poll_interval_seconds=60*60):
        print("=====================================================")
        print("   AUTONOMOUS TRADING DAEMON ONLINE   ")
        print(f"   Monitoring Core Pairs: {', '.join(self.pairs)}")
        print("   Status: Running seamlessly in the background.")
        
        if ENABLE_LIVE_EXECUTION and MT5_AVAILABLE:
            print("\n   MT5 LIVE EXECUTION: ENABLED (Connecting...)")
            if not mt5.initialize(login=MT5_LOGIN, server=MT5_SERVER, password=MT5_PASSWORD):
                print("   [CRITICAL] MT5 Initialization Failed! Correct your login credentials.")
                print("   Defaulting back to paper trading.")
                mt5.shutdown()
            else:
                print("   [SUCCESS] Connected to broker API successfully.")
        else:
            print("\n   MT5 LIVE EXECUTION: DISABLED (Paper Trading Only)")

        print("=====================================================")
        
        while True:
            try:
                self.poll_market()
                print(f"[*] Sleeping and monitoring for {poll_interval_seconds//60} minutes before next cycle...")
                time.sleep(poll_interval_seconds)
            except KeyboardInterrupt:
                print("\n[!] Daemon gracefully shutting down.")
                if MT5_AVAILABLE and ENABLE_LIVE_EXECUTION:
                    mt5.shutdown()
                break
            except Exception as e:
                print(f"[ERROR] Daemon encountered soft error: {e}")
                time.sleep(60) 

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None
    import warnings
    warnings.filterwarnings('ignore')
    
    CORE_PAIRS = ['BTC-USD', 'ETH-USD', 'GBPJPY=X']
    daemon = LiveTradingDaemon(pairs=CORE_PAIRS, interval='1h')
    
    # Run the background daemon infinitely, polling every 5 minutes
    daemon.start(poll_interval_seconds=300)
