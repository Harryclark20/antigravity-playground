import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

class PositionSizer:
    def __init__(self, default_risk_percent=1.0):
        self.default_risk_percent = default_risk_percent

    def calculate_lot_size(self, symbol: str, sl_distance: float, custom_risk=None) -> float:
        """
        Calculates the appropriate lot size based on account balance and stop loss distance.
        sl_distance should be in absolute price terms (e.g., 0.0050 for 50 pips on EURUSD).
        """
        if sl_distance <= 0:
            logger.warning("Invalid sl_distance provided for lot calculation.")
            return 0.01 # Minimum fallback

        risk_percent = custom_risk if custom_risk else self.default_risk_percent
        
        # Get account balance
        account_info = mt5.account_info()
        if account_info is None:
            logger.error("Failed to retrieve account info for lot size calculation.")
            return 0.01
            
        balance = account_info.balance
        risk_amount = balance * (risk_percent / 100)

        # Get symbol info for tick value
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Failed to retrieve symbol info for {symbol}.")
            return 0.01
            
        tick_size = symbol_info.trade_tick_size
        tick_value = symbol_info.trade_tick_value
        
        if tick_size == 0 or tick_value == 0:
            logger.error(f"Tick size or value is 0 for {symbol}.")
            return symbol_info.volume_min

        # Calculate how many ticks is the SL distance
        sl_ticks = sl_distance / tick_size
        
        if sl_ticks == 0:
            return symbol_info.volume_min
            
        # Value of 1 lot for the given stop loss distance
        sl_value_1_lot = sl_ticks * tick_value
        
        # Ideal lot size
        ideal_lot_size = risk_amount / sl_value_1_lot
        
        # Adjust to broker step and limits
        step_volume = symbol_info.volume_step
        min_volume = symbol_info.volume_min
        max_volume = symbol_info.volume_max
        
        # Round down to nearest step
        lot_size = (ideal_lot_size // step_volume) * step_volume
        
        # Clamp between min and max
        lot_size = max(min_volume, min(lot_size, max_volume))
        
        # Python float quirk: ensure the volume format is exactly the precision step implies (usually 2 decimals)
        precision = str(step_volume)[::-1].find('.')
        if precision > 0:
            lot_size = round(lot_size, precision)
            
        logger.debug(f"Calculated Lot Size: {lot_size} for Risk: ${risk_amount:.2f}, SL Ticks: {sl_ticks:.1f}")
        return lot_size
