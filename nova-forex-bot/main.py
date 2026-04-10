import time
from core.mt5_gateway import MT5Gateway

def main():
    print("--- Starting Nova Forex Bot (Fresh Start) ---")
    
    gateway = MT5Gateway()
    
    if gateway.connect():
        try:
            acc_info = gateway.get_account_info()
            if acc_info:
                print(f"Connection established! Balance: {acc_info['balance']} {acc_info['equity']}")
            
            print("Bot is now in 'Monitoring Mode'. Waiting for strategy integration...")
            
            # Main trading loop would go here
            while True:
                # print("Checking market conditions...")
                time.sleep(60) # Scan every minute
                
        except KeyboardInterrupt:
            print("Shutting down bot...")
        finally:
            gateway.shutdown()
    else:
        print("Could not start bot due to connection error.")

if __name__ == "__main__":
    main()
