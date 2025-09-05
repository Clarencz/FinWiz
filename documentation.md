# QuantApp Documentation

This document provides detailed technical documentation for the QuantApp project, covering its architecture, module functionalities, and implementation details.

## 1. Architecture Overview

QuantApp follows a modular architecture, separating concerns into distinct Python modules. This design promotes maintainability, scalability, and ease of development. The core application (`main.py`) acts as the central orchestrator, dispatching commands to specialized modules based on user input.

### Key Architectural Principles:

- **Modularity**: Each major feature or domain (e.g., data management, market data, analytics) is encapsulated within its own Python file/class.
- **CLI-driven**: The entire application is controlled via a command-line interface, built using the `click` library for robust command parsing and `prompt_toolkit` for enhanced user interaction (auto-completion, history).
- **Data Flow**: Data typically flows from external APIs or local files, through data management layers, into analysis/charting modules, and finally presented to the user or exported.
- **Separation of Concerns**: Different responsibilities (e.g., fetching data, performing calculations, rendering output) are handled by separate components.

## 2. Module Details

### `main.py`

This is the entry point of the application. It sets up the `click` command groups, initializes various manager classes, and handles the main command dispatching logic. It also integrates `prompt_toolkit` for an interactive shell experience.

**Key Responsibilities:**

- Defining top-level CLI commands (e.g., `stocks`, `crypto`, `portfolio`).
- Initializing instances of `DataManager`, `APIManager`, `DBManager`, `MarketData`, `CryptoData`, `ForexData`, `MacroData`, `Charting`, `Analytics`, `PortfolioManager`, `TradingSimulator`, `Reporting`, `ConfigManager`, and `SecurityManager`.
- Managing the application's state (e.g., currently loaded stock data).
- Handling command auto-completion and history.

### `data_manager.py`

Handles the import of data from various file formats.

**Class:** `DataManager`
**Methods:**

- `load_csv(file_path)`: Loads data from a CSV file into a pandas DataFrame.
- `load_excel(file_path)`: Loads data from an Excel file into a pandas DataFrame.
- `load_json(file_path)`: Loads data from a JSON file.

### `api_manager.py`

Manages interactions with external financial data APIs.

**Class:** `APIManager`
**Methods:**

- `get_yfinance_historical_data(ticker, period='1y', interval='1d')`: Fetches historical stock data using `yfinance`.
- _(Placeholder methods for Alpha Vantage, Polygon.io, Tiingo, FRED, CoinGecko APIs)_

### `db_manager.py`

Provides functionalities for interacting with a SQLite database for persistent data storage.

**Class:** `DBManager`
**Methods:**

- `connect()`: Establishes a connection to the SQLite database.
- `close()`: Closes the database connection.
- `save_dataframe(df, table_name, if_exists='replace')`: Saves a pandas DataFrame to a specified table.
- `load_dataframe(table_name)`: Loads data from a specified table into a pandas DataFrame.
- `execute_query(query)`: Executes a raw SQL query.
- `list_tables()`: Lists all tables in the database.

### `market_data.py`

Manages fetching and processing of equity market data.

**Class:** `MarketData`
**Methods:**

- `get_quote_snapshot(ticker)`: Retrieves a real-time quote snapshot for a given ticker.
- `get_ohlcv_history(ticker, period='1y', interval='1d')`: Fetches OHLCV historical data.
- `get_company_fundamentals(ticker)`: Retrieves company fundamental data.
- `get_financial_statements(ticker)`: Fetches financial statements (income, balance, cash flow).

### `crypto_data.py`

Handles fetching and processing of cryptocurrency data.

**Class:** `CryptoData`
**Methods:**

- `get_price_chart(coin_id, days=30)`: Fetches historical price charts for a cryptocurrency.
- `get_market_cap_rankings(top_n=10)`: Retrieves top cryptocurrency by market capitalization.
- _(Placeholder for on-chain metrics)_

### `forex_data.py`

Manages fetching and processing of foreign exchange data.

**Class:** `ForexData`
**Methods:**

- `get_live_rates(base_currency)`: Fetches live exchange rates.
- `get_historical_chart(base_currency, target_currency, days=30)`: Retrieves historical forex charts.

### `macro_data.py`

Handles fetching and processing of macroeconomic data.

**Class:** `MacroData`
**Methods:**

- `get_fred_series(series_id, api_key)`: Fetches data from FRED (Federal Reserve Economic Data).

### `charting.py`

Responsible for rendering terminal-based charts and visualizations.

**Class:** `Charting`
**Methods:**

- `plot_line_chart(data, title='Line Chart', xlabel='X-axis', ylabel='Y-axis')`: Plots a line chart using `plotext`.
- `plot_candlestick_chart(df, title='Candlestick Chart')`: Plots a candlestick chart (text-based).
- `display_table(df, title='Data Table')`: Displays a pandas DataFrame as a rich table with color-coding.

### `analytics.py`

Provides functions for quantitative and statistical analysis.

**Class:** `Analytics`
**Methods:**

- `calculate_technical_indicators(df)`: Calculates various technical indicators (SMA, EMA, WMA, RSI, MACD, Bollinger Bands) using `pandas_ta`.
- `display_technical_indicators(df)`: Displays a summary of calculated technical indicators.
- `calculate_correlations(df, columns=None)`: Computes and displays the correlation matrix.
- `calculate_volatility(df, column='Close', window=20)`: Calculates rolling volatility.
- `perform_regression_analysis(df, dependent_var, independent_vars)`: Performs linear regression using `statsmodels`.

### `portfolio_manager.py`

Manages portfolio creation, tracking, and analytics.

**Class:** `PortfolioManager`
**Methods:**

- `add_position(symbol, quantity, purchase_price)`: Adds a new position to the portfolio.
- `update_prices(market_data_source)`: Updates current prices for all holdings.
- `view_portfolio()`: Displays the current portfolio with gain/loss.
- `calculate_sharpe_ratio(returns, risk_free_rate=0.01)`: Calculates the Sharpe Ratio.
- `calculate_sortino_ratio(returns, risk_free_rate=0.01)`: Calculates the Sortino Ratio.
- `calculate_beta(stock_returns, market_returns)`: Calculates the Beta coefficient.
- `run_backtest(data, strategy_func)`: Runs a simple backtesting simulation.
- `plot_equity_curve(cumulative_returns, title='Equity Curve')`: Plots the equity curve.

### `trading_simulator.py`

Enables paper trading and tracks trade history.

**Class:** `TradingSimulator`
**Methods:**

- `buy(symbol, quantity, price)`: Simulates a buy order.
- `sell(symbol, quantity, price)`: Simulates a sell order.
- `view_balance()`: Displays current cash balance.
- `view_positions()`: Displays current open positions.
- `view_trade_history()`: Displays a history of all simulated trades.
- `connect_exchange_api(api_key, secret_key)`: Placeholder for real exchange API connection.
- `place_real_order(order_type, symbol, quantity, price=None)`: Placeholder for placing real orders.

### `reporting.py`

Handles generating reports and exporting data.

**Class:** `Reporting`
**Methods:**

- `export_dataframe_to_csv(df, file_path)`: Exports a DataFrame to CSV.
- `export_dataframe_to_excel(df, file_path)`: Exports a DataFrame to Excel.
- `generate_pdf_report(title, content, file_path)`: Generates a PDF report using `fpdf2`.
- _(Placeholder for email alerts and terminal notifications)_

### `config_manager.py`

Manages application settings, API keys, and command aliases.

**Class:** `ConfigManager`
**Methods:**

- `set(key, value)`: Sets a configuration value.
- `get(key)`: Retrieves a configuration value.
- `delete(key)`: Deletes a configuration value.
- `set_alias(alias, command)`: Sets a command alias.
- `get_alias(alias)`: Retrieves a command alias.
- `delete_alias(alias)`: Deletes a command alias.

### `security.py`

Provides functionalities for encrypting sensitive data.

**Class:** `SecurityManager`
**Methods:**

- `generate_key()`: Generates an encryption key.
- `load_key()`: Loads an encryption key from a file.
- `encrypt_data(data)`: Encrypts a string.
- `decrypt_data(encrypted_data)`: Decrypts an encrypted string.
- `encrypt_file(input_file, output_file)`: Encrypts a file.
- `decrypt_file(input_file, output_file)`: Decrypts a file.

## 3. Installation and Setup

Refer to the `README.md` file for detailed installation instructions and dependencies.

## 4. Usage and Commands

Refer to the `README.md` file for basic usage and a list of core commands.

## 5. Extending QuantApp

Due to its modular design, extending QuantApp is straightforward:

- **Adding New Data Sources**: Create a new method in `api_manager.py` or a new dedicated data module (e.g., `etf_data.py`) to fetch data from a new API. Integrate it into `main.py` as a new command.
- **Implementing New Indicators/Analytics**: Add new functions to `analytics.py` to implement new technical indicators or statistical models. Ensure they operate on pandas DataFrames for compatibility.
- **New Chart Types**: Extend `charting.py` with methods to render new types of terminal-based visualizations.
- **Trading Strategies**: Develop new trading strategies within `trading_simulator.py` or as separate functions that can be passed to the `run_backtest` method in `portfolio_manager.py`.

## 6. Testing

Unit tests are located in `test_quant_app.py` and cover the core functionalities of each module. To run tests:

```bash
python3 -m unittest test_quant_app.py
```

## 7. Future Enhancements

- **Real-time Data Streaming**: Implement live data feeds for continuous updates.
- **Advanced Backtesting Engine**: Develop a more sophisticated backtesting framework with detailed performance metrics and optimization capabilities.
- **Machine Learning Integration**: Incorporate predictive models for forecasting and anomaly detection.
- **Web-based UI**: Explore the possibility of a lightweight web interface for visualization and interaction.
- **More API Integrations**: Expand support for additional financial data providers.
- **Multi-threading/Asynchronous Operations**: Improve performance for data-intensive tasks.

---
