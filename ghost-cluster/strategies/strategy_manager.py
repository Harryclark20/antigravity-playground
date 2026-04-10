import pandas_ta as ta

class StrategyManager:
    def __init__(self):
        self.strategies = {}
        self.active_strategy = None

    def add_strategy(self, name, strategy):
        self.strategies[name] = strategy

    def prepare_data(self, df):
        # Calculate market regime indicators (ADX)
        df.ta.adx(length=14, append=True)
        # Prepare data for all underlying strategies
        for s in self.strategies.values():
            s.prepare_data(df)

    def evaluate(self, index, row, df_history):
        # Dynamically adopt strategy based on market condition
        adx_value = row.get('ADX_14', 0)
        
        if adx_value > 25:
            # Trending Market -> Use Momentum/Sniper Strategy
            self.active_strategy = self.strategies.get('momentum')
        else:
            # Ranging Market -> Use Mean Reversion Strategy
            self.active_strategy = self.strategies.get('mean_reversion')
            
        if self.active_strategy:
            return self.active_strategy.generate_signal(index, row, df_history)
            
        return {'action': 'HOLD'}
