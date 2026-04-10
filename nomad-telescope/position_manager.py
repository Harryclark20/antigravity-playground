import MetaTrader5 as mt5
import logging

class PositionManager:
    def __init__(self):
        pass
        
    def move_to_breakeven(self, symbol, min_pips_profit=10):
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            return
            
        for pos in positions:
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                continue
            point = symbol_info.point
            
            if pos.type == mt5.ORDER_TYPE_BUY:
                profit_pips = (pos.price_current - pos.price_open) / point
                if profit_pips >= min_pips_profit and pos.sl < pos.price_open:
                    new_sl = pos.price_open + (1 * point)
                    self._modify_sl(pos.ticket, pos.symbol, new_sl, pos.tp)
                    
            elif pos.type == mt5.ORDER_TYPE_SELL:
                profit_pips = (pos.price_open - pos.price_current) / point
                if profit_pips >= min_pips_profit and (pos.sl > pos.price_open or pos.sl == 0):
                    new_sl = pos.price_open - (1 * point)
                    self._modify_sl(pos.ticket, pos.symbol, new_sl, pos.tp)
                    
    def _modify_sl(self, ticket, symbol, sl, tp):
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": symbol,
            "sl": float(sl),
            "tp": float(tp)
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Failed to move SL for {ticket}: {result.comment}")
        else:
            logging.info(f"Successfully moved SL to breakeven for {ticket}")
