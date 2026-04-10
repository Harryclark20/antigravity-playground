from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import MetaTrader5 as mt5
import asyncio
import logging
import os
import time

# Import actual bot config and logic
import config
from main import TradingAdvisor

app = FastAPI(title="Elite Hybrid Forex Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust logging for the API
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('API_Logger')

class Credentials(BaseModel):
    account: int
    password: str
    server: str

# Global state
bot_task = None
bot_loop = None
is_running = False

@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "Forex Bot Backend API is active."}

@app.get("/api/test")
def test_api():
    logger.info("Test endpoint hit")
    return {"status": "ok", "time": time.time()}

@app.post("/api/connect")
def connect_mt5(creds: Credentials):
    global is_running
    logger.info(f"Connection request received for account: {creds.account}")
    
    try:
        # Update config memory
        config.MT5_ACCOUNT = creds.account
        config.MT5_PASSWORD = creds.password
        config.MT5_SERVER = creds.server
        
        logger.info("Initializing MT5...")
        if not mt5.initialize():
            err = mt5.last_error()
            logger.error(f"MT5 Init failed: {err}")
            raise HTTPException(status_code=500, detail=f"MT5 Init failed: {err}")
            
        logger.info("Attempting MT5 login...")
        if not mt5.login(creds.account, password=creds.password, server=creds.server):
            err = mt5.last_error()
            logger.error(f"MT5 Login failed: {err}")
            raise HTTPException(status_code=500, detail=f"MT5 Login failed: {err}")
            
        logger.info("Connection successful")
        return {"message": "Successfully connected to MetaTrader 5."}
    except Exception as e:
        logger.error(f"Unexpected error in connect_mt5: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
def get_status():
    status_data = {
        "connected": False,
        "bot_running": is_running,
        "balance": 0.0,
        "equity": 0.0,
        "active_trades": 0
    }
    
    # Only pull data if mt5 says we are structurally sound
    if mt5.terminal_info() is not None:
        status_data["connected"] = True
        acc_info = mt5.account_info()
        if acc_info:
            status_data["balance"] = acc_info.balance
            status_data["equity"] = acc_info.equity
            
        positions = mt5.positions_get()
        if positions is not None:
            # Filter specifically for the bot's magic number if you want, or show all
            status_data["active_trades"] = len([p for p in positions if p.magic == 100100])
            
    return status_data

def run_bot_in_background():
    global bot_loop, is_running
    is_running = True
    
    bot = TradingAdvisor()
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    
    try:
        bot_loop.run_until_complete(bot.run())
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Bot loop crashed: {e}")
    finally:
        is_running = False
        bot_loop.close()

@app.post("/api/start")
def start_bot(background_tasks: BackgroundTasks):
    global is_running
    
    # Check connect
    if mt5.terminal_info() is None:
        raise HTTPException(status_code=400, detail="Connect to MT5 first.")
        
    if is_running:
        return {"message": "Bot is already running."}
        
    background_tasks.add_task(run_bot_in_background)
    return {"message": "Bot startup initiated."}

@app.post("/api/stop")
def stop_bot():
    global bot_loop, is_running
    
    if not is_running:
        return {"message": "Bot is not running."}
        
    if bot_loop and bot_loop.is_running():
        bot_loop.call_soon_threadsafe(bot_loop.stop)
        
    is_running = False
    return {"message": "Bot stopped successfully."}

@app.get("/api/logs")
def get_logs(lines: int = 50):
    log_path = os.path.join(config.LOGS_DIR, "bot.log")
    if not os.path.exists(log_path):
        return {"logs": ["No logs yet."]}
        
    try:
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
            return {"logs": all_lines[-lines:]}
    except Exception as e:
        return {"logs": [f"Error reading logs: {e}"]}
