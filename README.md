# QuantApp: A Text-Based Terminal Quant Application

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Features](#2-features)
3.  [Installation](#3-installation)
4.  [Usage](#4-usage)
5.  [Modules Overview](#5-modules-overview)
    - [Core App Structure](#core-app-structure)
    - [Data Import & Management](#data-import--management)
    - [Market Data Modules](#market-data-modules)
    - [Charting & Visuals](#charting--visuals)
    - [Quant & Analytics](#quant--analytics)
    - [Trading & Simulation](#trading--simulation)
    - [Reporting & Export](#reporting--export)
    - [Usability Enhancements](#usability-enhancements)
    - [Security](#security)
6.  [Contributing](#6-contributing)
7.  [License](#7-license)

## 1. Introduction

QuantApp is a comprehensive text-based terminal application built in Python, designed for quantitative analysis, market data exploration, and trading simulation. It provides a command-line interface (CLI) for users to interact with various financial data sources, perform technical and statistical analysis, visualize data in the terminal, and simulate trading strategies.

This application aims to provide a lightweight yet powerful tool for financial enthusiasts, students, and professionals who prefer a terminal-centric workflow for their quantitative tasks.

## 2. Features

QuantApp offers a wide range of features, categorized into the following modules:

- **Core App Structure**: CLI-based navigation, modular design, command auto-completion & history, configurable settings.
- **Data Import & Management**: Manual file imports (CSV, Excel, JSON), API imports (Yahoo Finance, Alpha Vantage, Polygon.io, Tiingo, FRED, CoinGecko), database integration (SQLite/PostgreSQL), live streaming mode.
- **Market Data Modules**: Equities (load ticker, quote snapshot, OHLCV history, company fundamentals, financial statements), Crypto (price charts, market cap rankings, on-chain metrics), Forex (live rates, historical charts), Macroeconomic (inflation rates, GDP, interest rates, employment data).
- **Charting & Visuals (Terminal-based)**: ASCII or rich-rendered line charts, candlestick charts (text-based or pop-out Matplotlib), tables with color-coded gain/loss, heatmaps.
- **Quant & Analytics**: Technical Analysis (Moving Averages, RSI, MACD, Bollinger Bands, Support & Resistance), Statistical Analysis (Correlations, Volatility, Regression), Portfolio Analytics (Risk metrics, Performance vs. benchmark), Backtesting (simple strategy testing, equity curve chart), Machine Learning (optional future: predictive models).
- **Trading & Simulation**: Paper trading (simulate trades, order tracking), Exchange API integration (optional: Alpaca, Interactive Brokers).
- **Reporting & Export**: Export to CSV/Excel, PDF reports with performance charts, email alerts, terminal notifications.
- **Usability Enhancements**: Rich text UI, color-coded displays, auto-complete commands, command aliases, help system, themes.
- **Security**: Local storage encryption for API keys, optional login/authentication, sandbox mode.

## 3. Installation

To install QuantApp, follow these steps: ensure you have microsoft build tools(msvc) installed in your windows system to procede:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quantapp.git
    cd quantapp
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    _(Note: A `requirements.txt` file will be generated in the future. For now, install the following packages manually: `click`, `rich`, `prompt-toolkit`, `plotext`, `yfinance`, `pandas_ta`, `cryptography`, `requests`, `pandas`, `numpy`, `fpdf2`, `beautifulsoup4`, `statsmodels`)_

## 4. Usage

To start the QuantApp, run the `main.py` script from your terminal:

```bash
python3 main.py
```

Once the application starts, you will be presented with a command prompt. You can type `help` to see a list of available commands.

### Basic Commands:

- `help [command]`: Displays help information for a specific command or lists all commands.
- `stocks load <TICKER>`: Loads historical data for a given stock ticker (e.g., `stocks load AAPL`).
- `stocks chart`: Displays a chart for the currently loaded stock.
- `crypto load <COIN>`: Loads data for a given cryptocurrency (e.g., `crypto load BTC`).
- `portfolio view`: Displays your current portfolio.
- `exit`: Exits the application.

### Configuration:

API keys and other settings can be configured using the `config` commands. For example:

- `config set api_key <YOUR_API_KEY>`: Sets an API key.
- `config get api_key`: Retrieves a stored API key.

## 5. Modules Overview

This section provides a detailed overview of the different modules within QuantApp.

### Core App Structure

The core of QuantApp is built around a `click`-based CLI, providing a robust and extensible command-line interface. It supports nested commands, auto-completion (via `prompt_toolkit`), and command history. The application is designed with modularity in mind, allowing for easy expansion and maintenance of different financial domains.

### Data Import & Management

QuantApp handles data through `DataManager`, `APIManager`, and `DBManager`.

- **Manual File Imports**: Supports loading data from CSV, Excel, and JSON files for backtesting or custom analysis.
- **API Imports**: Integrates with various financial APIs to fetch live and historical data:
  - **Yahoo Finance (`yfinance`)**: For equities data.
  - **CoinGecko (`requests`)**: For cryptocurrency data.
  - **FRED (`requests`)**: For macroeconomic data.
  - _(Future integrations: Alpha Vantage, Polygon.io, Tiingo for broader coverage)._
- **Database Integration**: Uses SQLite (`db_manager.py`) for local storage of historical data, enabling faster access and offline analysis. PostgreSQL integration is planned for larger datasets.
- **Live Streaming Mode**: (Planned) Will allow streaming of real-time prices for selected assets.

### Market Data Modules

Dedicated modules manage data for different asset classes:

- **Equities (`market_data.py`)**: Provides functions to load stock tickers, retrieve quote snapshots, fetch OHLCV (Open, High, Low, Close, Volume) history, and access company fundamentals and financial statements.
- **Crypto (`crypto_data.py`)**: Offers functionalities for fetching cryptocurrency price charts, market capitalization rankings, and on-chain metrics.
- **Forex (`forex_data.py`)**: Manages live exchange rates and historical currency charts.
- **Macroeconomic (`macro_data.py`)**: Integrates with sources like FRED to retrieve inflation rates, GDP, interest rates, and employment data.

### Charting & Visuals

Visualizations are rendered directly in the terminal using `plotext` and `rich`.

- **Line Charts**: ASCII or rich-rendered line charts for price trends.
- **Candlestick Charts**: Possible in text via `plotext` or in pop-out `matplotlib` windows for more detailed analysis.
- **Tables with Color-Coded Gain/Loss**: Financial tables are enhanced with `rich` to display gains in green and losses in red for quick visual interpretation.
- **Heatmaps**: (Planned) For visualizing sector performance or other matrix-based data.

### Quant & Analytics

The `analytics.py` module provides a suite of quantitative tools:

- **Technical Analysis (`pandas_ta`)**: Calculates popular indicators such as Moving Averages (SMA, EMA, WMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Bollinger Bands. Basic support and resistance detection is also included.
- **Statistical Analysis**: Includes functions for calculating correlations between assets, measuring volatility, and performing regression analysis (`statsmodels`).
- **Portfolio Analytics**: (Implemented in `portfolio_manager.py`) Calculates key risk metrics like Sharpe Ratio, Sortino Ratio, and Beta, and evaluates portfolio performance against benchmarks.
- **Backtesting**: A simplified framework for testing trading strategies using historical data, with the ability to plot equity curves.
- **Machine Learning**: (Future) Integration of predictive models for price forecasting and anomaly detection.

### Trading & Simulation

The `trading_simulator.py` module enables simulated trading activities:

- **Paper Trading**: Users can simulate buying and selling assets with a virtual balance, tracking open orders and trade history.
- **Order Tracking**: Comprehensive logging of all simulated trades.
- **Exchange API Integration**: (Optional, planned) Future versions may allow connection to real brokerage APIs like Alpaca or Interactive Brokers for live trading.

### Reporting & Export

QuantApp provides robust reporting capabilities through `reporting.py`:

- **Export to CSV/Excel**: Easily export dataframes to common spreadsheet formats.
- **PDF Reports**: Generate professional PDF reports with performance charts and key metrics using `fpdf2`.
- **Email Alerts**: (Planned) Send automated email notifications for significant market events or portfolio changes.
- **Terminal Notifications**: Color-coded pop-ups for important alerts within the terminal.

### Usability Enhancements

User experience is a key focus:

- **Rich Text UI**: Leverages the `rich` library for enhanced terminal output, including color-coded gains/losses, highlighted warnings, and errors.
- **Auto-complete Commands**: Powered by `prompt_toolkit` for efficient command entry.
- **Command Aliases**: Users can define custom aliases for frequently used commands.
- **Help System**: Detailed `help` commands for each module and function.
- **Themes**: Configurable dark/light color profiles and minimal/detailed views.

### Security

Security features are implemented to protect sensitive information:

- **Local Storage Encryption**: API keys and other sensitive configurations are encrypted using `cryptography` before being stored locally.
- **Optional Login/Authentication**: (Planned) For multi-user environments or enhanced security.
- **Sandbox Mode**: (Planned) For safely testing code or strategies without affecting live data or real trading accounts.

## 6. Contributing

Contributions are welcome! Please feel free to submit issues, pull requests, or suggest new features. See `CONTRIBUTING.md` (planned) for more details.

## 7. License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---
