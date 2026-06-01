# Binance Futures Testnet Trading Bot (USDT-M)

A production-quality Python 3.11+ Command Line Interface (CLI) application for placing orders on the **Binance Futures Testnet (USDT-M)**. Built with high reliability, robust validation, structural logging, and modular architecture.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Architecture and Separation of Concerns](#architecture-and-separation-of-concerns)
4. [Installation & Virtual Environment Setup](#installation--virtual-environment-setup)
5. [Binance Futures Testnet Setup](#binance-futures-testnet-setup)
6. [Environment Variable Configuration](#environment-variable-configuration)
7. [Supported Features & Validations](#supported-features--validations)
8. [Example Commands](#example-commands)
9. [Sample CLI Outputs](#sample-cli-outputs)
10. [Logging System](#logging-system)
11. [Assumptions & Design Choices](#assumptions--design-choices)

---

## 🔍 Project Overview

This utility provides active traders and developers with a robust tool to interface directly with the Binance Futures Testnet. It allows developers to test their strategies or execute manually structured orders safely without risking real capital. It supports three order types:
* `MARKET` - Immediate execution at the best available price.
* `LIMIT` - Placement of orders at a specific target limit price (requires price, defaults to Good 'Til Cancelled `GTC`).
* `STOP_MARKET` - Execution of a market order triggered once the index/mark price reaches a custom threshold (requires stop-price).

---

## 📂 Folder Structure

The application strictly implements clean separation of concerns and follows the directory structure shown below:

```text
trading_bot/
│
├── bot/
│   ├── __init__.py          # Marks bot as a Python package, defines version info
│   ├── client.py            # Loads environment configs and initializes the Binance client
│   ├── orders.py            # Standardizes and dispatches MARKET, LIMIT, STOP_MARKET orders
│   ├── validators.py        # Strict validators for symbols, quantities, prices, sides
│   ├── logging_config.py    # Standardizes rotating file logging & beautiful console logs
│   └── cli.py               # Orchestrates CLI arguments, exception handling, and UI output
│
├── logs/
│   └── trading_bot.log      # Active rotating file logs with millisecond timestamps
│
├── .env                     # Local configuration credentials (ignored from VCS)
├── .env.example             # Template file demonstrating expected variables
├── README.md                # Comprehensive documentation and runner instructions
└── requirements.txt         # Pinned production library dependencies
```

---

## 🏛️ Architecture and Separation of Concerns

* **`bot/validators.py`**: Ensures all arguments passed via CLI are validated locally before touching the network. This saves bandwidth, speeds up API interaction, and prevents unnecessary API rate-limit penalization from Binance for malformed requests.
* **`bot/client.py`**: Is responsible exclusively for system configurations, loading credential states from `.env`, and initializing a secure, testnet-bound `python-binance` client.
* **`bot/orders.py`**: Interacts with the API, maps custom domain terms onto Binance endpoint parameters, parses structural fields, and formats raw JSON payloads into human-readable structures.
* **`bot/logging_config.py`**: Automatically generates directories and ensures that every interaction has an audit trail.
* **`bot/cli.py`**: Interfaces directly with the operating system terminal, parses commands, executes the orchestrator, and catches structural exceptions to output elegant terminal error prompts.

---

## 🛠️ Installation & Virtual Environment Setup

This project requires **Python 3.11+**. Follow the steps below to initialize and configure the application on your local machine:

### 1. Clone or Move into the Project Directory
```bash
cd trading_bot
```

### 2. Create a Virtual Environment
Initialize a clean environment (`venv`):
```bash
# On Windows
python -m venv venv

# On macOS/Linux
python3 -m venv venv
```

### 3. Activate the Virtual Environment
```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
.\venv\Scripts\activate.bat

# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
Install the required libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 🌐 Binance Futures Testnet Setup

1. Navigate to the [Binance Futures Testnet Portal](https://testnet.binancefuture.com).
2. Log in using your Binance account (or register a testnet account).
3. Click on the **"API Key"** tab in the mock dashboard.
4. Generate a new API Key and Secret Key. Save them securely.
5. In your mock dashboard, ensure you have allocated mock balance (e.g. USDT) to trade.

---

## ⚙️ Environment Variable Configuration

Create a copy of `.env.example` named `.env` in the root of the `trading_bot` directory:

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

Open the newly created `.env` file and insert your credentials:
```env
BINANCE_API_KEY=your_binance_testnet_api_key_here
BINANCE_API_SECRET=your_binance_testnet_api_secret_here
```

---

## 🛡️ Supported Features & Validations

The application performs local client validations:
* **Symbol format**: Must be uppercase alphanumeric (e.g., `BTCUSDT`, `ETHUSDT`) between 3 and 20 characters.
* **Quantity**: Must be a valid floating-point number strictly greater than `0`.
* **Side**: Must be `BUY` or `SELL` (case-insensitive, normalized automatically).
* **Order type**: Must be `MARKET`, `LIMIT`, or `STOP_MARKET` (case-insensitive, normalized automatically).
* **Price Validation**: Required and must be greater than `0` for `LIMIT` orders; must NOT be specified for `MARKET` or `STOP_MARKET` orders.
* **Stop Price Validation**: Required and must be greater than `0` for `STOP_MARKET` orders; must NOT be specified for `MARKET` or `LIMIT` orders.

---

## 🚀 Example Commands

Ensure your virtual environment is active and you are in the root directory `trading_bot`.

### 1. Place a MARKET BUY Order
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### 2. Place a LIMIT SELL Order
```bash
python -m bot.cli --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 120000
```

### 3. Place a STOP_MARKET BUY Order (Bonus Feature)
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --order-type STOP_MARKET --quantity 0.001 --stop-price 98500
```

---

## 📊 Sample CLI Outputs

### Sample 1: Successful LIMIT Order Execution
```text
[20:12:05] INFO: Logging configured successfully. Logs saved to: .../trading_bot/logs/trading_bot.log
[20:12:05] INFO: Starting Binance Futures Testnet CLI...
[20:12:05] INFO: Validating input parameters...
[20:12:05] INFO: Parameters validated successfully.
[20:12:05] INFO: Initializing python-binance client on Binance Futures Testnet...
[20:12:06] INFO: --- Order Request Summary ---
[20:12:06] INFO: Symbol:      BTCUSDT
[20:12:06] INFO: Side:        SELL
[20:12:06] INFO: Type:        LIMIT
[20:12:06] INFO: Quantity:    0.001
[20:12:06] INFO: Price:       120000.0
[20:12:06] INFO: Parameters:  {'symbol': 'BTCUSDT', 'side': 'SELL', 'type': 'LIMIT', 'quantity': 0.001, 'price': 120000.0, 'timeInForce': 'GTC'}
[20:12:06] INFO: -----------------------------
[20:12:06] INFO: Executing order on Binance Futures Testnet...
[20:12:07] INFO: API Response received successfully.
[20:12:07] INFO: Order Placed - ID: 284729105, Status: NEW, Executed Qty: 0.0, Avg Price: 120000.0

==================================================
🔥 ORDER REQUEST SUMMARY 🔥
==================================================
Symbol:      BTCUSDT
Side:        SELL
Order Type:  LIMIT
Quantity:    0.001
Price:       120000.0

==================================================
📦 BINANCE API RESPONSE 📦
==================================================
{
  "orderId": 284729105,
  "symbol": "BTCUSDT",
  "status": "NEW",
  "clientOrderId": "android_90ab38c...",
  "price": "120000.00",
  "avgPrice": "0.00000",
  "origQty": "0.001",
  "executedQty": "0.000",
  "cumQty": "0.000",
  "cumQuote": "0.00000",
  "timeInForce": "GTC",
  "type": "LIMIT",
  "reduceOnly": false,
  "closePosition": false,
  "side": "SELL",
  "positionSide": "BOTH",
  "stopPrice": "0.00",
  "workingType": "CONTRACT_PRICE",
  "priceProtect": false,
  "origType": "LIMIT",
  "updateTime": 1775133605000
}

==================================================
📈 ORDER EXECUTION RESULT SUMMARY 📈
==================================================
Order ID:     284729105
Status:       NEW
Executed Qty: 0.000
Avg Price:    120000.00
Result:       ✅ Order 284729105 placed successfully with status: NEW.
==================================================
```

### Sample 2: Validation Failure Output
```text
[20:15:32] INFO: Logging configured successfully. Logs saved to: .../trading_bot/logs/trading_bot.log
[20:15:32] INFO: Starting Binance Futures Testnet CLI...
[20:15:32] INFO: Validating input parameters...
[20:15:32] ERROR: Validation failed: Stop price (--stop-price) is required for STOP_MARKET orders.

❌ Validation Error: Stop price (--stop-price) is required for STOP_MARKET orders.
```

---

## 📝 Logging System

All events are securely appended to `logs/trading_bot.log` as structured log entries:
1. **Timestamp**: Local ISO 8601 formatting (`YYYY-MM-DD HH:MM:SS`).
2. **Standard Headers**: Logging level (`INFO`/`ERROR`/`WARNING`/`DEBUG`) and module context.
3. **Audit details**:
   * Request parameters summary (pre-execution).
   * Exact configuration status.
   * Remote server execution timestamps and detailed API outcomes.
   * Full traceback references for generic execution crashes.

---

## 📌 Assumptions & Design Choices

1. **Leverage `/fapi` endpoints**: The bot maps exclusively onto USDT-M Futures endpoints. All functions use prefix `futures_` from the `python-binance` library.
2. **Leverage `timeInForce='GTC'`**: Limit orders on Binance require a TIF specification. We use `GTC` (Good 'Til Cancelled) as the standard default to maximize fills without premature order expiration.
3. **Local Parameter Pre-filtering**: We validate input constraints locally first. This protects users' API accounts from being blocked due to excessive spamming of invalid payloads.
4. **Quantities and Step-Size Rules**: Symbol minimum precision limits (e.g. quantity decimals) vary by symbol on Binance. This application forwards precision parameters exactly as passed by the user. Ensure your `--quantity` respects symbol specific decimals (e.g. `0.001` for BTCUSDT) to avoid API rejecting the order.
