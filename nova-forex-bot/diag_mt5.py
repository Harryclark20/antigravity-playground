import MetaTrader5 as mt5
import datetime

def diagnose():
    if not mt5.initialize():
        print(f"Failed to initialize: {mt5.last_error()}")
        return

    print(f"Connect status: {mt5.terminal_info().connected}")
    
    # Check selection
    selected = mt5.symbol_select("EURUSD", True)
    print(f"EURUSD Selected: {selected}")
    
    # Try fetching ticks from 24 hours ago
    start = datetime.datetime.now() - datetime.timedelta(days=1)
    ticks = mt5.copy_ticks_from("EURUSD", start, 100, mt5.COPY_TICKS_ALL)
    if ticks is not None:
        print(f"Ticks from 24h ago: {len(ticks)}")
    else:
        print(f"copy_ticks_from(24h ago) returned None. Error: {mt5.last_error()}")

    # Try fetching 100 M1 candles
    rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M1, 0, 100)
    if rates is not None:
        print(f"M1 Candles found: {len(rates)}")
    else:
        print(f"M1 Candles error: {mt5.last_error()}")

    mt5.shutdown()

if __name__ == "__main__":
    diagnose()
