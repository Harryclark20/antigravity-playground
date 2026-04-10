class SignalVoter:
    def __init__(self, min_votes=3):
        self.min_votes = min_votes

    def evaluate(self, strategy_results: dict) -> dict:
        """
        Takes a dictionary of strategy results and counts the votes.
        'weight' can be optionally passed in the result dict to give more power to a strategy.
        """
        buy_votes = 0.0
        sell_votes = 0.0
        buy_confidence = 0.0
        sell_confidence = 0.0
        
        buy_sl_distances = []
        buy_tp_distances = []
        sell_sl_distances = []
        sell_tp_distances = []

        for name, result in strategy_results.items():
            signal = result.get('signal', 'NO_TRADE')
            weight = float(result.get('weight', 1.0))  # Default weight of 1.0
            confidence = float(result.get('confidence', 0.0))
            scored_confidence = weight * confidence

            if signal == 'BUY':
                buy_votes += weight
                buy_confidence += scored_confidence
                if result.get('sl_distance'):
                    buy_sl_distances.append(result['sl_distance'])
                if result.get('tp_distance'):
                    buy_tp_distances.append(result['tp_distance'])
                elif result.get('tp_price') and result.get('sl_distance'):
                    buy_tp_distances.append(result['sl_distance'] * 2.5)
            elif signal == 'SELL':
                sell_votes += weight
                sell_confidence += scored_confidence
                if result.get('sl_distance'):
                    sell_sl_distances.append(result['sl_distance'])
                if result.get('tp_distance'):
                    sell_tp_distances.append(result['tp_distance'])
                elif result.get('tp_price') and result.get('sl_distance'):
                    sell_tp_distances.append(result['sl_distance'] * 2.5)

        final_signal = 'NO_TRADE'
        final_sl = 0.0
        final_tp = 0.0

        if buy_votes >= self.min_votes and buy_votes > sell_votes:
            final_signal = 'BUY'
            final_sl = sum(buy_sl_distances) / len(buy_sl_distances) if buy_sl_distances else 0.0
            final_tp = sum(buy_tp_distances) / len(buy_tp_distances) if buy_tp_distances else 0.0
        elif sell_votes >= self.min_votes and sell_votes > buy_votes:
            final_signal = 'SELL'
            final_sl = sum(sell_sl_distances) / len(sell_sl_distances) if sell_sl_distances else 0.0
            final_tp = sum(sell_tp_distances) / len(sell_tp_distances) if sell_tp_distances else 0.0

        return {
            'signal': final_signal,
            'votes': max(buy_votes, sell_votes) if final_signal != 'NO_TRADE' else 0,
            'confidence': (buy_confidence if final_signal == 'BUY' else (sell_confidence if final_signal == 'SELL' else 0.0)),
            'sl_distance': final_sl,
            'tp_distance': final_tp
        }
