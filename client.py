"""
Binance API Client Wrapper Module.

Handles loading environment variables and configuring/instantiating
the python-binance client specifically for the Binance Futures Testnet.
"""

import os
import logging
from typing import Tuple
from dotenv import load_dotenv
from binance.client import Client


class ClientError(Exception):
    """Base exception for client-related errors."""
    pass


class ConfigurationError(ClientError):
    """Raised when environment variables or configuration options are missing or invalid."""
    pass


def load_credentials() -> Tuple[str, str]:
    """
    Loads and validates Binance API credentials from the environment.
    
    Tries to find the .env file and extracts BINANCE_API_KEY and BINANCE_API_SECRET.
    
    Returns:
        A tuple of (api_key, api_secret).
        
    Raises:
        ConfigurationError: If any environment variable is missing or empty.
    """
    # Load environment variables from .env
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    errors = []
    if not api_key:
        errors.append("BINANCE_API_KEY is not defined or is empty in .env.")
    if not api_secret:
        errors.append("BINANCE_API_SECRET is not defined or is empty in .env.")
        
    if errors:
        error_msg = " Configuration Error: " + " ".join(errors)
        logging.error(error_msg)
        raise ConfigurationError(error_msg)
        
    # Strip whitespace to avoid issues
    return api_key.strip(), api_secret.strip()


def get_binance_client() -> Client:
    """
    Initializes and returns a python-binance client set up for Futures Testnet.
    
    Returns:
        An instantiated binance.client.Client configured for testnet.
        
    Raises:
        ConfigurationError: If environment variables are missing.
        ClientError: If initialization fails.
    """
    api_key, api_secret = load_credentials()
    
    logging.info("Initializing python-binance client on Binance Futures Testnet...")
    
    try:
        # Initializing the python-binance Client.
        # Passing testnet=True configures the client to route both Spot and
        # Futures requests to their respective Testnet URLs.
        # Futures Testnet Base URL: https://testnet.binancefuture.com
        client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        return client
    except Exception as err:
        error_msg = f"Failed to initialize Binance Client: {err}"
        logging.error(error_msg)
        raise ClientError(error_msg) from err
