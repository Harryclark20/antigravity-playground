import customtkinter as ctk
import tkinter as tk
import MetaTrader5 as mt5
import threading
import asyncio
import sys
import logging
from datetime import datetime

# We will import these dynamically after setting config
import config

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

class ForexBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Elite Hybrid Forex Bot")
        self.geometry("900x600")
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.bot_thread = None
        self.bot_loop = None
        
        self.create_sidebar()
        self.create_main_frame()
        
    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FX Bot Control", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.account_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="MT5 Account")
        self.account_entry.grid(row=1, column=0, padx=20, pady=10)
        
        self.password_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10)
        
        self.server_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Broker Server")
        self.server_entry.grid(row=3, column=0, padx=20, pady=10)
        
        self.connect_btn = ctk.CTkButton(self.sidebar_frame, text="Connect MT5", command=self.connect_mt5)
        self.connect_btn.grid(row=4, column=0, padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="Status: Disconnected", text_color="red")
        self.status_label.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Dashboard Top
        self.dash_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.dash_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.balance_label = ctk.CTkLabel(self.dash_frame, text="Balance: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.balance_label.pack(side="left", padx=20)
        
        self.equity_label = ctk.CTkLabel(self.dash_frame, text="Equity: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        self.equity_label.pack(side="left", padx=20)

        self.start_bot_btn = ctk.CTkButton(self.dash_frame, text="START BOT", fg_color="green", hover_color="darkgreen", command=self.start_bot, state="disabled")
        self.start_bot_btn.pack(side="right", padx=10)
        
        self.stop_bot_btn = ctk.CTkButton(self.dash_frame, text="STOP BOT", fg_color="red", hover_color="darkred", command=self.stop_bot, state="disabled")
        self.stop_bot_btn.pack(side="right", padx=10)

        # Logging Text Box
        self.log_textbox = ctk.CTkTextbox(self.main_frame, state="disabled")
        self.log_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Setup logging
        text_handler = TextHandler(self.log_textbox)
        logger = logging.getLogger()
        logger.addHandler(text_handler)
        logger.setLevel(logging.INFO)

    def connect_mt5(self):
        acc = self.account_entry.get()
        pwd = self.password_entry.get()
        srv = self.server_entry.get()
        
        if not acc or not pwd or not srv:
            logging.error("Please fill in all MT5 credentials.")
            return
            
        try:
            acc = int(acc)
        except:
            logging.error("Account must be an integer.")
            return

        # Initialize MT5 here just to test connection
        if not mt5.initialize():
            logging.error(f"MT5 initialization failed: {mt5.last_error()}")
            return
            
        if not mt5.login(acc, password=pwd, server=srv):
            logging.error(f"MT5 login failed: {mt5.last_error()}")
            return
            
        logging.info("Successfully connected to MetaTrader 5!")
        self.status_label.configure(text="Status: Connected", text_color="green")
        
        # Update config module with new credentials so bot picks it up
        config.MT5_ACCOUNT = acc
        config.MT5_PASSWORD = pwd
        config.MT5_SERVER = srv
        
        # Fetch initial account info
        account_info = mt5.account_info()
        if account_info:
            self.balance_label.configure(text=f"Balance: ${account_info.balance:.2f}")
            self.equity_label.configure(text=f"Equity: ${account_info.equity:.2f}")
            
        # Enable start button
        self.start_bot_btn.configure(state="normal")
        self.connect_btn.configure(state="disabled")
        
    def start_bot(self):
        logging.info("Starting Autonomous Trading Bot...")
        self.start_bot_btn.configure(state="disabled")
        self.stop_bot_btn.configure(state="normal")
        
        # Import main modules dynamically now that config is updated
        # It's important to do it here so they pick up the in-memory config changes
        def run_bot_thread():
            import sys
            # Remove from modules if already imported so it re-evaluates 'from config import ...'
            for mod in list(sys.modules.keys()):
                if mod.startswith('data.') or mod.startswith('strategies.') or mod.startswith('execution.') or mod.startswith('main'):
                    del sys.modules[mod]
                    
            from main import TradingAdvisor
            bot = TradingAdvisor()
            
            self.bot_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.bot_loop)
            try:
                self.bot_loop.run_until_complete(bot.run())
            except asyncio.CancelledError:
                pass
            finally:
                self.bot_loop.close()

        self.bot_thread = threading.Thread(target=run_bot_thread, daemon=True)
        self.bot_thread.start()
        
        # Start a loop to update balance visually
        self.update_dashboard()

    def update_dashboard(self):
        if self.bot_loop and self.bot_loop.is_running():
            acc = mt5.account_info()
            if acc:
                self.balance_label.configure(text=f"Balance: ${acc.balance:.2f}")
                self.equity_label.configure(text=f"Equity: ${acc.equity:.2f}")
            self.after(2000, self.update_dashboard)

    def stop_bot(self):
        logging.info("Stopping Bot...")
        if self.bot_loop and self.bot_loop.is_running():
            self.bot_loop.call_soon_threadsafe(self.bot_loop.stop)
            
        self.start_bot_btn.configure(state="normal")
        self.stop_bot_btn.configure(state="disabled")
        logging.info("Bot Stopped.")

if __name__ == "__main__":
    app = ForexBotGUI()
    app.mainloop()
