import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

class TradeManager:
    def __init__(self, break_even_ratio=1.0, trailing_atr_multiplier=2.0):
        # Move SL to BE when price reaches X ratio of the original SL distance
        self.break_even_ratio = break_even_ratio
        # Trail behind price by X ATR
        self.trailing_atr_multiplier = trailing_atr_multiplier

    def manage_positions(self, symbol: str, current_price: float, current_atr: float = 0.0):
        """
        Manages open positions. Moves Stop Losses to break-even or trails them.
        """
        positions = mt5.positions_get(symbol=symbol)
        if positions is None or len(positions) == 0:
            return

        for pos in positions:
            if pos.magic != 100100:  # Only manage our bot's trades
                continue

            sl = pos.sl
            tp = pos.tp
            open_price = pos.price_open
            ticket = pos.ticket
            
            # Initial SL Distance
            initial_sl_dist = abs(open_price - sl) if sl > 0 else 0
            
            if initial_sl_dist == 0:
                continue

            # Calculate Break-Even Trigger Point
            be_trigger_dist = initial_sl_dist * self.break_even_ratio
            
            # For BUY
            if pos.type == mt5.ORDER_TYPE_BUY:
                current_profit_dist = current_price - open_price
                
                # Trail Stop Logic
                if current_atr > 0.0:
                    new_sl = current_price - (current_atr * self.trailing_atr_multiplier)
                    
                    # 1. Trailing Stop
                    if new_sl > sl and new_sl > open_price: # Only trail upwards, and ideally locked above open
                        self._modify_sl(ticket, pos.symbol, new_sl, tp)
                        continue
                        
                # 2. Break Even Logic (if trailing doesn't trigger)
                if current_profit_dist >= be_trigger_dist and sl < open_price:
                    # Move to break-even + small spread buffer
                    be_price = open_price + (mt5.symbol_info(pos.symbol).spread * mt5.symbol_info(pos.symbol).point)
                    self._modify_sl(ticket, pos.symbol, be_price, tp)
                    
            # For SELL
            elif pos.type == mt5.ORDER_TYPE_SELL:
                current_profit_dist = open_price - current_price
                
                # Trail Stop Logic
                if current_atr > 0.0:
                    new_sl = current_price + (current_atr * self.trailing_atr_multiplier)
                    
                    # 1. Trailing Stop
                    if (sl == 0 or new_sl < sl) and new_sl < open_price: # Only trail downwards
                        self._modify_sl(ticket, pos.symbol, new_sl, tp)
                        continue
                        
                # 2. Break Even Logic
                if current_profit_dist >= be_trigger_dist and (sl > open_price or sl == 0):
                    be_price = open_price - (mt5.symbol_info(pos.symbol).spread * mt5.symbol_info(pos.symbol).point)
                    self._modify_sl(ticket, pos.symbol, be_price, tp)

    def _modify_sl(self, ticket: int, symbol: str, new_sl: float, tp: float):
        """Helper to send MT5 modification requests safely."""
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": symbol,
            "sl": float(new_sl),
            "magic": 100100
        }
        if tp > 0.0:
            request["tp"] = float(tp)
            
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Failed to modify SL/TP for ticket {ticket}. Retcode: {result.retcode}")
        else:
            logger.info(f"Successfully modified SL for ticket {ticket} to {new_sl}")
