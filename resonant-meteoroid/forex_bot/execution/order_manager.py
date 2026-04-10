import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, max_spread_points=25, slippage_points=5):
        self.max_spread_points = max_spread_points
        self.slippage = slippage_points

    def _check_spread(self, symbol: str) -> bool:
        """Verifies the current spread is within acceptable limits."""
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Cannot retrieve info for {symbol} to check spread.")
            return False
            
        spread = symbol_info.spread
        if spread > self.max_spread_points:
            logger.warning(f"Spread for {symbol} is too high: {spread} > {self.max_spread_points}. Trade aborted.")
            return False
            
        return True

    def execute_trade(self, symbol: str, signal: str, lot_size: float, sl_price: float = 0.0, tp_price: float = 0.0) -> dict:
        """
        Executes a market order.
        signal: 'BUY' or 'SELL'.
        """
        if signal not in ['BUY', 'SELL']:
            return {"success": False, "reason": "Invalid Signal"}

        if not self._check_spread(symbol):
            return {"success": False, "reason": "Spread Too High"}

        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                logger.error(f"Symbol {symbol} not found or failed to select.")
                return {"success": False, "reason": "Symbol Not Selected"}

        order_type = mt5.ORDER_TYPE_BUY if signal == 'BUY' else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).ask if signal == 'BUY' else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot_size),
            "type": order_type,
            "price": float(price),
            "deviation": self.slippage,
            "magic": 100100, # Magic number to identify bot trades
            "comment": "AI Hybrid Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC, # Immediate or Cancel is standard for MT5 market orders depending on broker
        }

        if sl_price > 0:
            request["sl"] = float(sl_price)
        if tp_price > 0:
            request["tp"] = float(tp_price)

        # Send order
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order send failed! Retcode: {result.retcode}. Comment: {result.comment}")
            return {"success": False, "reason": result.comment, "retcode": result.retcode}

        logger.info(f"Successfully executed {signal} on {symbol} - Volume {lot_size}. Ticket: {result.order}")
        return {"success": True, "ticket": result.order, "price": result.price}

    def close_position(self, ticket: int) -> bool:
        """Close an open position completely by its ticket number."""
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            logger.error(f"Position {ticket} not found.")
            return False
            
        pos = position[0]
        close_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": pos.ticket,
            "price": price,
            "deviation": self.slippage,
            "magic": 100100,
            "comment": "Bot manual close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Close order failed! Retcode: {result.retcode}. Comment: {result.comment}")
            return False
            
        logger.info(f"Position {ticket} closed successfully. Profit: {pos.profit}")
        return True
