import pandas as pd
from core.data_feed import DataFeed
from core.bot import Bot
from strategies.strategy_manager import StrategyManager
from strategies.mean_reversion import MeanReversionStrategy
from strategies.ict_momentum import ICTMomentumStrategy

def run_backtest_on_pair(pair, days=60):
    manager = StrategyManager()
    manager.add_strategy('mean_reversion', MeanReversionStrategy())
    manager.add_strategy('momentum', ICTMomentumStrategy())

    data_feed = DataFeed(symbol=pair, interval='1h', days_back=days)
    df = data_feed.fetch_data(silent=True)
    if df.empty:
        return None
        
    bot = Bot(data_feed=data_feed, strategy_manager=manager, initial_balance=10000.0)
    trades, final_balance = bot.run_simulation()
    
    wins = len([t for t in trades if t['pnl'] > 0])
    losses = len([t for t in trades if t['pnl'] <= 0])
    total = len(trades)
    win_rate = (wins/total)*100 if total > 0 else 0
    total_return = ((final_balance-10000)/10000)*100
    
    return {
        'total': total,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'return_pct': total_return,
        'final_balance': final_balance
    }

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None
    import warnings
    warnings.filterwarnings('ignore')

    CORE_PAIRS = ['BTC-USD', 'ETH-USD', 'GBPJPY=X']
    print("=========================================================")
    print("         AUTONOMOUS PORTFOLIO BACKTEST RUNNER            ")
    print(f"         Spanning {len(CORE_PAIRS)} Core Assets over 60 Days")
    print("=========================================================\n")
    
    total_start = 10000.0 * len(CORE_PAIRS)
    total_end = 0.0
    
    for pair in CORE_PAIRS:
        print(f"[*] Running full historical backtest for {pair}...")
        results = run_backtest_on_pair(pair)
        
        if not results:
            print(f"    [!] Failed to pull sufficient data for {pair}.\n")
            continue
            
        print(f"    -> Net Return: {results['return_pct']:.2f}% | Win Rate: {results['win_rate']:.1f}% "
              f"({results['wins']}W / {results['losses']}L)")
        print(f"    -> Final Balance: ${results['final_balance']:.2f}\n")
        
        total_end += results['final_balance']
        
    print("=========================================================")
    print("                AGGREGATE PERFORMANCE                    ")
    print("=========================================================")
    print(f" Total Portfolio Initial Capital: ${total_start:,.2f}")
    print(f" Total Portfolio Ending Capital:  ${total_end:,.2f}")
    net_profit = total_end - total_start
    print(f" Net Profit:                      ${net_profit:,.2f} ({((total_end-total_start)/total_start)*100:.2f}%)")
    print("=========================================================")
