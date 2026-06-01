"""
Input Validation Module.

Defines validation functions to ensure order arguments conform to strict business
rules before sending requests to the Binance API.
"""

import re
from typing import Optional


class ValidationError(ValueError):
    """Custom exception raised when validation checks fail."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validates the trading symbol format (e.g., BTCUSDT).
    
    Symbol must be an uppercase alphanumeric string containing between 3 and 20 characters.
    
    Args:
        symbol: The symbol string to validate.
        
    Returns:
        The validated uppercase symbol.
        
    Raises:
        ValidationError: If the symbol is invalid.
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    
    # Normalize to uppercase
    normalized_symbol = symbol.strip().upper()
    
    # Standard Binance Futures symbols are uppercase alphanumeric (e.g. BTCUSDT, 1000LUNCUSDT)
    pattern = r"^[A-Z0-9]{3,20}$"
    if not re.match(pattern, normalized_symbol):
        raise ValidationError(
            f"Invalid symbol format '{symbol}'. "
            f"Must be uppercase alphanumeric (e.g., BTCUSDT) between 3 and 20 characters."
        )
        
    return normalized_symbol


def validate_quantity(quantity_str: str) -> float:
    """
    Validates that the quantity is a positive number.
    
    Args:
        quantity_str: The quantity value as a string.
        
    Returns:
        The validated quantity as a float.
        
    Raises:
        ValidationError: If quantity is not a valid float or is <= 0.
    """
    if not quantity_str:
        raise ValidationError("Quantity cannot be empty.")
    
    try:
        quantity = float(quantity_str)
    except ValueError as err:
        raise ValidationError(f"Quantity must be a numeric value, got '{quantity_str}'.") from err
        
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than zero, got {quantity}.")
        
    return quantity


def validate_side(side: str) -> str:
    """
    Validates that the order side is either BUY or SELL.
    
    Args:
        side: The order side string to validate.
        
    Returns:
        The validated uppercase side string.
        
    Raises:
        ValidationError: If the side is not BUY or SELL.
    """
    if not side:
        raise ValidationError("Order side cannot be empty.")
        
    normalized_side = side.strip().upper()
    if normalized_side not in ("BUY", "SELL"):
        raise ValidationError(f"Invalid order side '{side}'. Must be 'BUY' or 'SELL'.")
        
    return normalized_side


def validate_order_type(order_type: str) -> str:
    """
    Validates that the order type is one of the supported types.
    
    Supported types: MARKET, LIMIT, STOP_MARKET.
    
    Args:
        order_type: The order type string to validate.
        
    Returns:
        The validated uppercase order type.
        
    Raises:
        ValidationError: If the order type is unsupported.
    """
    if not order_type:
        raise ValidationError("Order type cannot be empty.")
        
    normalized_type = order_type.strip().upper()
    supported_types = ("MARKET", "LIMIT", "STOP_MARKET")
    if normalized_type not in supported_types:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Supported types: {', '.join(supported_types)}."
        )
        
    return normalized_type


def validate_price(price_str: Optional[str], order_type: str) -> Optional[float]:
    """
    Validates the price parameter.
    
    Price is REQUIRED and must be > 0 for LIMIT orders.
    For other order types, price must not be specified.
    
    Args:
        price_str: The price value as a string (or None).
        order_type: The validated order type (LIMIT, MARKET, STOP_MARKET).
        
    Returns:
        The validated price as a float, or None if price is not required.
        
    Raises:
        ValidationError: If rules are violated or price is invalid.
    """
    normalized_type = order_type.strip().upper()
    
    if normalized_type == "LIMIT":
        if price_str is None or price_str.strip() == "":
            raise ValidationError("Price is required for LIMIT orders.")
        
        try:
            price = float(price_str)
        except ValueError as err:
            raise ValidationError(f"Price must be a numeric value, got '{price_str}'.") from err
            
        if price <= 0:
            raise ValidationError(f"Price must be greater than zero, got {price}.")
        return price
        
    # For MARKET and STOP_MARKET, price is not needed/supported by standard order endpoints
    if price_str is not None and price_str.strip() != "":
        raise ValidationError(f"Price should not be specified for {normalized_type} orders.")
        
    return None


def validate_stop_price(stop_price_str: Optional[str], order_type: str) -> Optional[float]:
    """
    Validates the stop_price parameter for STOP_MARKET orders.
    
    Stop price is REQUIRED and must be > 0 for STOP_MARKET orders.
    For other order types, stop price must not be specified.
    
    Args:
        stop_price_str: The stop price value as a string (or None).
        order_type: The validated order type (LIMIT, MARKET, STOP_MARKET).
        
    Returns:
        The validated stop price as a float, or None if stop price is not required.
        
    Raises:
        ValidationError: If rules are violated or stop price is invalid.
    """
    normalized_type = order_type.strip().upper()
    
    if normalized_type == "STOP_MARKET":
        if stop_price_str is None or stop_price_str.strip() == "":
            raise ValidationError("Stop price (--stop-price) is required for STOP_MARKET orders.")
            
        try:
            stop_price = float(stop_price_str)
        except ValueError as err:
            raise ValidationError(f"Stop price must be a numeric value, got '{stop_price_str}'.") from err
            
        if stop_price <= 0:
            raise ValidationError(f"Stop price must be greater than zero, got {stop_price}.")
        return stop_price
        
    if stop_price_str is not None and stop_price_str.strip() != "":
        raise ValidationError(f"Stop price should not be specified for {normalized_type} orders.")
        
    return None
