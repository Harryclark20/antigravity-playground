import pandas as pd

class RegimeDetector:
    def __init__(self, adx_trend_threshold=25, bb_narrow_threshold=0.002):
        self.adx_trend_threshold = adx_trend_threshold
        self.bb_narrow_threshold = bb_narrow_threshold

    def detect(self, df: pd.DataFrame) -> str:
        """
        Detects the current market regime based on the latest data.
        Returns one of: 'TREND', 'RANGE', 'VOLATILE', 'LOW VOLATILITY'
        """
        if df is None or df.empty:
            return "UNKNOWN"

        # Look at the most recent completed candle (index -1, or if -1 is forming, -2)
        # Assuming the last row is the latest confirmed data.
        current = df.iloc[-1]
        
        # Look back slightly to detect spikes
        if len(df) > 20:
            atr_history = df['ATR'].iloc[-20:-1]
            atr_mean = atr_history.mean()
            atr_std = atr_history.std()
        else:
            atr_mean = current['ATR']
            atr_std = 0
            
        is_atr_spike = current['ATR'] > (atr_mean + 1.5 * atr_std) if atr_std > 0 else False
        
        # Evaluate Bollinger Band bandwidth
        # Depending on asset, BB_bandwidth could be absolute or relative. 
        # Using a relative approach using recent history is safer across pairs.
        if len(df) > 20:
            bb_history = df['BB_bandwidth'].iloc[-20:-1]
            bb_mean = bb_history.mean()
        else:
            bb_mean = current['BB_bandwidth']

        is_bb_narrow = current['BB_bandwidth'] < (bb_mean * 0.8) # 20% tighter than recent mean

        is_trending = current['ADX'] > self.adx_trend_threshold
        
        if is_atr_spike:
            return "VOLATILE"
        elif is_bb_narrow and not is_trending:
            return "LOW VOLATILITY" if is_bb_narrow and current['ATR'] < atr_mean else "RANGE"
        elif is_trending:
            return "TREND"
        else:
            # Default fallback when ADX is low and no volatility spike
            return "RANGE"
