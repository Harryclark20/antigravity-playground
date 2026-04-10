class BaseStrategy:
    def __init__(self, name):
        self.name = name

    def generate_signal(self, current_bar, df_history):
        """
        Returns a dictionary:
        {
          'action': 'BUY' | 'SELL' | 'HOLD',
          'entry': float,
          'sl': float,
          'tp': float
        }
        """
        return {'action': 'HOLD'}
