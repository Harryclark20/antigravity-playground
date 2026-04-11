import telebot
import json
import threading

class TelegramAgent:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)['telegram']
        
        self.enabled = self.config.get('enabled', False)
        self.bot = None
        self.on_command_callback = None
        
        if self.enabled:
            self.bot = telebot.TeleBot(self.config['token'])
            self._setup_handlers()
            self.thread = threading.Thread(target=self._start_polling, daemon=True)
            self.thread.start()
            print("Telegram Agent initialized and polling...")

    def _start_polling(self):
        try:
            self.bot.infinity_polling()
        except Exception as e:
            print(f"Telegram Polling Error: {e}")

    def _setup_handlers(self):
        @self.bot.message_handler(commands=['status'])
        def handle_status(message):
            if str(message.chat.id) == str(self.config['chat_id']):
                if self.on_command_callback:
                    self.on_command_callback("status")

        @self.bot.message_handler(commands=['pause'])
        def handle_pause(message):
            if str(message.chat.id) == str(self.config['chat_id']):
                if self.on_command_callback:
                    self.on_command_callback("pause")
                self.send_alert("🔴 TRADING HALTED via Remote Command.")

    def send_alert(self, text):
        """Sends an outbound notification to your phone."""
        if self.enabled and self.bot:
            try:
                self.bot.send_message(self.config['chat_id'], text)
            except Exception as e:
                print(f"Failed to send Telegram alert: {e}")

    def register_callback(self, callback):
        """Allows the main loop to register a handler for incoming commands."""
        self.on_command_callback = callback
