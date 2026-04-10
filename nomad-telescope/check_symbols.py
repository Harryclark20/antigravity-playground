import MetaTrader5 as mt5
import config
if mt5.initialize(login=config.MT5_LOGIN, password=config.MT5_PASSWORD, server=config.MT5_SERVER):
    symbols = mt5.symbols_get()
    print("Total symbols:", len(symbols))
    crypto_keywords = ['BTC', 'ETH', 'SOL', 'CRYPTO']
    found = []
    for s in symbols:
        for kw in crypto_keywords:
            if kw in s.name.upper():
                found.append(s.name)
    print("Found Crypto Symbols:", list(set(found)))
    mt5.shutdown()
