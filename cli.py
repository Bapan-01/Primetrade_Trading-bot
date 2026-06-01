"""
Command Line Interface (CLI) Entry Point.

Parses CLI arguments, performs validations, triggers order execution,
and displays order request/response summaries.
"""

import sys
import argparse
import logging
import json
from typing import List, Optional

# Local imports
from bot.logging_config import setup_logging
from bot.validators import (
    validate_symbol,
    validate_quantity,
    validate_side,
    validate_order_type,
    validate_price,
    validate_stop_price,
    ValidationError
)
from bot.client import get_binance_client, ConfigurationError, ClientError
from bot.orders import OrderManager, OrderExecutionError


def parse_arguments(args: List[str]) -> argparse.Namespace:
    """
    Parses CLI arguments for the trading bot order placement.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        An argparse.Namespace containing parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures Testnet (USDT-M) with ease.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)."
    )
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL."
    )
    parser.add_argument(
        "--order-type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET", "market", "limit", "stop_market"],
        help="Order type: MARKET, LIMIT, or STOP_MARKET."
    )
    parser.add_argument(
        "--quantity",
        type=str,
        required=True,
        help="Order quantity (e.g., 0.001)."
    )
    parser.add_argument(
        "--price",
        type=str,
        required=False,
        default=None,
        help="Limit price (required for LIMIT orders, must be > 0)."
    )
    parser.add_argument(
        "--stop-price",
        type=str,
        required=False,
        default=None,
        help="Stop price (required for STOP_MARKET orders, must be > 0)."
    )
    
    return parser.parse_args(args)


def run_bot(args_list: List[str]) -> int:
    """
    Orchestrates validation, client setup, order execution, and result display.
    
    Args:
        args_list: System command-line arguments list.
        
    Returns:
        Status code (0 for success, 1 for failure).
    """
    # 1. Initialize logging
    setup_logging()
    
    logging.info("Starting Binance Futures Testnet CLI...")
    
    # 2. Parse arguments
    try:
        parsed_args = parse_arguments(args_list)
    except SystemExit:
        # argparse handles printing help and errors, exit with code 1
        return 1

    # 3. Validate input parameters
    logging.info("Validating input parameters...")
    try:
        # Convert and validate standard values
        symbol = validate_symbol(parsed_args.symbol)
        side = validate_side(parsed_args.side)
        order_type = validate_order_type(parsed_args.order_type)
        quantity = validate_quantity(parsed_args.quantity)
        
        # Cross-validation based on order type
        price = validate_price(parsed_args.price, order_type)
        stop_price = validate_stop_price(parsed_args.stop_price, order_type)
        
        logging.info("Parameters validated successfully.")
        
    except ValidationError as err:
        logging.error("Validation failed: %s", err)
        print(f"\n❌ Validation Error: {err}", file=sys.stderr)
        return 1

    # 4. Initialize Binance client
    try:
        client = get_binance_client()
    except ConfigurationError as err:
        print(f"\n❌ Configuration Error: {err}", file=sys.stderr)
        print("💡 Hint: Ensure you have a .env file configured with correct variables.", file=sys.stderr)
        return 1
    except ClientError as err:
        print(f"\n❌ Client Initialization Error: {err}", file=sys.stderr)
        return 1

    # 5. Execute Order Placement
    try:
        manager = OrderManager(client)
        result = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        # 6. Display Result Summary beautifully
        print("\n" + "=" * 50)
        print("🔥 ORDER REQUEST SUMMARY 🔥")
        print("=" * 50)
        print(f"Symbol:      {symbol}")
        print(f"Side:        {side}")
        print(f"Order Type:  {order_type}")
        print(f"Quantity:    {quantity}")
        if price is not None:
            print(f"Price:       {price}")
        if stop_price is not None:
            print(f"Stop Price:  {stop_price}")
        
        print("\n" + "=" * 50)
        print("📦 BINANCE API RESPONSE 📦")
        print("=" * 50)
        # Pretty print the raw response dictionary
        print(json.dumps(result["raw_response"], indent=2))
        
        print("\n" + "=" * 50)
        print("📈 ORDER EXECUTION RESULT SUMMARY 📈")
        print("=" * 50)
        print(f"Order ID:     {result['orderId']}")
        print(f"Status:       {result['status']}")
        print(f"Executed Qty: {result['executedQty']}")
        print(f"Avg Price:    {result['avgPrice']}")
        print(f"Result:       ✅ {result['message']}")
        print("=" * 50 + "\n")
        
        return 0

    except OrderExecutionError as err:
        print(f"\n❌ Order Execution Failed: {err}", file=sys.stderr)
        return 1
    except Exception as err:
        logging.error("An unexpected error occurred during execution: %s", err, exc_info=True)
        print(f"\n❌ Unexpected Fatal Error: {err}", file=sys.stderr)
        return 1


def main() -> None:
    """Main package CLI entry point."""
    sys.exit(run_bot(sys.argv[1:]))


if __name__ == "__main__":
    main()
