"""
Logging Configuration Module.

Configures logging for the trading bot, sending output to both the console
and a rolling file log located in the 'logs/' folder.
"""

import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """
    Configures the root logger for both console and file output.
    
    Logs will be output to console at INFO level, and written to
    'logs/trading_bot.log' with file rotation.
    """
    # Determine the project root directory relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    logs_dir = os.path.join(project_root, "logs")
    
    # Ensure logs directory exists
    os.makedirs(logs_dir, exist_ok=True)
    
    log_file_path = os.path.join(logs_dir, "trading_bot.log")
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear any pre-existing handlers
    root_logger.handlers.clear()
    
    # 1. File Handler (with size-based rotation)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # 2. Console Handler (for real-time CLI feedback)
    console_formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries (e.g., urllib3, binance)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("binance").setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully. Logs saved to: %s", log_file_path)
