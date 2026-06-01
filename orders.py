"""
Order Placement Module.

Provides classes and helper methods to build order requests, execute them
using the Binance Futures Client, handle API errors, and parse the responses.
"""

import logging
from typing import Any, Dict, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException


class OrderExecutionError(Exception):
    """Raised when an order placement fails due to API, network, or other errors."""
    pass


class OrderManager:
    """
    Manages building and placing orders on Binance Futures (USDT-M) Testnet.
    """

    def __init__(self, client: Client) -> None:
        """
        Initializes the OrderManager with a configured Binance client.
        
        Args:
            client: An active, authenticated binance.client.Client.
        """
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Builds, logs, and executes an order on the Binance Futures Testnet.
        
        Args:
            symbol: Alphanumeric trading pair, e.g., 'BTCUSDT'.
            side: 'BUY' or 'SELL'.
            order_type: 'MARKET', 'LIMIT', or 'STOP_MARKET'.
            quantity: Order quantity.
            price: Required for LIMIT orders, otherwise None.
            stop_price: Required for STOP_MARKET orders, otherwise None.
            
        Returns:
            A dictionary containing the standardized order summary and raw response.
            
        Raises:
            OrderExecutionError: If the order fails to execute due to validation,
                                  authentication, or API issues.
        """
        # 1. Structure the request parameters
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good 'til Cancelled (standard default)
        elif order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        # 2. Log Order Request Summary
        logging.info("--- Order Request Summary ---")
        logging.info("Symbol:      %s", symbol)
        logging.info("Side:        %s", side)
        logging.info("Type:        %s", order_type)
        logging.info("Quantity:    %s", quantity)
        if price is not None:
            logging.info("Price:       %s", price)
        if stop_price is not None:
            logging.info("Stop Price:  %s", stop_price)
        logging.info("Parameters:  %s", params)
        logging.info("-----------------------------")

        try:
            # 3. Call Binance Futures Testnet API
            logging.info("Executing order on Binance Futures Testnet...")
            response = self.client.futures_create_order(**params)
            
            # 4. Log API Response
            logging.info("API Response received successfully.")
            logging.debug("Raw Response: %s", response)
            
            # 5. Extract and parse response fields
            order_id = response.get("orderId")
            status = response.get("status")
            executed_qty = response.get("executedQty", "0.0")
            avg_price = response.get("avgPrice")
            
            # If avgPrice is "0" or "0.00000", fallback to "price" or "N/A"
            if avg_price and float(avg_price) > 0:
                avg_price_display = str(avg_price)
            elif response.get("price") and float(response.get("price")) > 0:
                avg_price_display = str(response.get("price"))
            else:
                avg_price_display = "N/A"

            summary = {
                "success": True,
                "message": f"Order {order_id} placed successfully with status: {status}.",
                "orderId": order_id,
                "status": status,
                "executedQty": executed_qty,
                "avgPrice": avg_price_display,
                "raw_response": response
            }
            
            logging.info("Order Placed - ID: %s, Status: %s, Executed Qty: %s, Avg Price: %s",
                         order_id, status, executed_qty, avg_price_display)
            return summary

        except BinanceAPIException as err:
            error_msg = f"Binance API Exception [{err.code}]: {err.message}"
            logging.error(error_msg)
            logging.debug("API Exception Details: %s", err)
            raise OrderExecutionError(error_msg) from err

        except BinanceRequestException as err:
            error_msg = f"Binance Request Exception (Network issue): {err}"
            logging.error(error_msg)
            raise OrderExecutionError(error_msg) from err

        except Exception as err:
            error_msg = f"Unexpected exception placing order: {err}"
            logging.error(error_msg)
            raise OrderExecutionError(error_msg) from err
