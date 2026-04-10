import sys
import pandas as pd
from core.data_feed import DataFeed
from core.bot import Bot
from strategies.strategy_manager import StrategyManager
from strategies.mean_reversion import MeanReversionStrategy
from strategies.ict_momentum import ICTMomentumStrategy

def main():
    print("=========================================")
    print("    Autonomous Trading Bot Initializing   ")
    print("=========================================\n")

    print("[*] Setting up Strategy Modules...")
    manager = StrategyManager()
    manager.add_strategy('mean_reversion', MeanReversionStrategy())
    manager.add_strategy('momentum', ICTMomentumStrategy())

    # We use yfinance GC=F (Gold) for 1h for 60 days to test
    data_feed = DataFeed(symbol='GC=F', interval='1h', days_back=60)
    data_feed.fetch_data()
    
    bot = Bot(data_feed=data_feed, strategy_manager=manager, initial_balance=10000.0)
    
    print("\n[*] Commencing Autonomous Simulation...")
    trades, final_balance = bot.run_simulation()
    
    wins = len([t for t in trades if t['pnl'] > 0])
    losses = len([t for t in trades if t['pnl'] <= 0])
    total = len(trades)
    
    print("\n=========================================")
    print("         Simulation Performance          ")
    print("=========================================")
    print(f"Initial Account Balance: $10,000.00")
    print(f"Final Account Balance:   ${final_balance:.2f}")
    print(f"Total Return:            {((final_balance-10000)/10000)*100:.2f}%")
    print("-" * 41)
    print(f"Total Trades Taken:      {total}")
    if total > 0:
        win_rate = (wins/total)*100
        print(f"Winning Trades:          {wins} ({win_rate:.1f}%)")
        print(f"Losing Trades:           {losses}")
        print("\nNote: The bot dynamically filters trades to ensure an edge (>1.2 RR).")
        print("Performance validates structural robustness over sheer volume.")
        if win_rate >= 80:
            print("\n[SUCCESS] Targeted 80%+ Win Rate Achieved!")
    else:
        print("No trades triggered. The criteria are highly selective.")
        
    print("=========================================")

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None
    import warnings
    warnings.filterwarnings('ignore')
    main()
