#!/usr/bin/env python3
"""
Quant Terminal Application
A comprehensive text-based terminal quant application with CLI navigation,
market data modules, charting, analytics, and trading simulation capabilities.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
import json
import time

# Import DataManager, APIManager, DBManager, MarketData, CryptoData, ForexData, MacroData, Charting, Analytics, PortfolioManager, TradingSimulator, Reporting, ConfigManager, and SecurityManager
from data_manager import DataManager
from api_manager import APIManager
from db_manager import DBManager
from market_data import MarketData
from crypto_data import CryptoData
from forex_data import ForexData
from macro_data import MacroData
from charting import Charting
from analytics import Analytics
from portfolio_manager import PortfolioManager
from trading_simulator import TradingSimulator
from reporting import Reporting
from config_manager import ConfigManager
from security import SecurityManager

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

console = Console()

# Define a history file for prompt_toolkit
HISTORY_FILE = os.path.join(os.path.expanduser("~/.quant_app_history"))

# Global session for prompt_toolkit
session = PromptSession(history=FileHistory(HISTORY_FILE))

# Command completer for prompt_toolkit
# This will be dynamically updated based on available commands
command_completer = WordCompleter([], ignore_case=True)

# Initialize managers
data_manager = DataManager()
api_manager = APIManager()
db_manager = DBManager()
market_data = MarketData()
crypto_data = CryptoData()
forex_data = ForexData()
macro_data = MacroData()
charting = Charting()
analytics = Analytics()
portfolio_manager = PortfolioManager()
trading_simulator = TradingSimulator()
reporting = Reporting()
config_manager = ConfigManager()
security_manager = SecurityManager()

# Global variable to store loaded stock data
current_stock_data = None

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A comprehensive text-based terminal quant application."""
    ctx.ensure_object(dict)
    ctx.obj["CONFIG_MANAGER"] = config_manager
    ctx.obj["DATA_MANAGER"] = data_manager
    ctx.obj["API_MANAGER"] = api_manager
    ctx.obj["DB_MANAGER"] = db_manager
    ctx.obj["MARKET_DATA"] = market_data
    ctx.obj["CRYPTO_DATA"] = crypto_data
    ctx.obj["FOREX_DATA"] = forex_data
    ctx.obj["MACRO_DATA"] = macro_data
    ctx.obj["CHARTING"] = charting
    ctx.obj["ANALYTICS"] = analytics
    ctx.obj["PORTFOLIO_MANAGER"] = portfolio_manager
    ctx.obj["TRADING_SIMULATOR"] = trading_simulator
    ctx.obj["REPORTING"] = reporting
    ctx.obj["SECURITY_MANAGER"] = security_manager
    ctx.obj["CURRENT_STOCK_DATA"] = current_stock_data

    if ctx.invoked_subcommand is None:
        show_welcome()
    
    # Update the command completer with available commands
    commands = list(cli.commands.keys())
    for group in [stocks, crypto, forex, macro, portfolio, config, import_data, db, analyze, trade, report, security]:
        if isinstance(group, click.Group):
            commands.extend([f"{group.name} {cmd}" for cmd in group.commands.keys()])
    command_completer.words = sorted(list(set(commands)))

def show_welcome():
    """Display welcome message and available commands."""
    console.print(Panel.fit(
        "[bold blue]Welcome to Quant Terminal[/bold blue]\n"
        "A comprehensive financial analysis and trading platform",
        title="[bold green]Financial Wizard[/bold green]"
    ))
    
    table = Table(title="Available Commands")
    table.add_column("Command", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    table.add_row("help", "Show this help message")
    table.add_row("stocks", "Stock market data and analysis")
    table.add_row("crypto", "Cryptocurrency data and analysis")
    table.add_row("forex", "Foreign exchange data")
    table.add_row("macro", "Macroeconomic data")
    table.add_row("portfolio", "Portfolio management")
    table.add_row("config", "Configuration settings")
    table.add_row("import", "Import data from files")
    table.add_row("db", "Database management commands")
    table.add_row("analyze", "Quantitative analysis and technical indicators")
    table.add_row("trade", "Trading simulation and order management")
    table.add_row("report", "Reporting and export features")
    table.add_row("security", "Security features (encryption, authentication)")
    table.add_row("exit", "Exit the application")
    
    console.print(table)
    console.print("\n[yellow]Type (\[command] --help) for more information on a specific command.[/yellow]")

@cli.command()
def help():
    """Show help message and available commands."""
    show_welcome()

@cli.group()
def stocks():
    """Stock market data and analysis commands."""
    pass

@stocks.command()
@click.argument("ticker")
@click.pass_context
def load(ctx, ticker):
    """Load stock data for a given ticker."""
    global current_stock_data
    console.print(f"[green]Loading stock data for {ticker.upper()}...[/green]")
    df = ctx.obj["API_MANAGER"].get_yfinance_historical_data(ticker)
    if df is not None:
        current_stock_data = df
        console.print(f"[green]Successfully loaded historical data for {ticker.upper()}. Shape: {df.shape}[/green]")
        console.print(df.tail())
    else:
        console.print(f"[bold red]Error:[/bold red] Could not load data for {ticker.upper()}.")

@stocks.command()
@click.argument("ticker")
@click.pass_context
def quote(ctx, ticker):
    """Get a snapshot quote for a given ticker."""
    console.print(f"[green]Fetching quote snapshot for {ticker.upper()}...[/green]")
    ctx.obj["MARKET_DATA"].get_quote_snapshot(ticker)

@stocks.command()
@click.argument("ticker")
@click.option("--period", default="1y", help="Period for historical data (e.g., 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max).")
@click.option("--interval", default="1d", help="Interval for historical data (e.g., 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo).")
@click.pass_context
def history(ctx, ticker, period, interval):
    """Get OHLCV historical data for a given ticker."""
    console.print(f"[green]Fetching OHLCV history for {ticker.upper()}...[/green]")
    ctx.obj["MARKET_DATA"].get_ohlcv_history(ticker, period, interval)

@stocks.command()
@click.argument("ticker")
@click.pass_context
def fundamentals(ctx, ticker):
    """Get company fundamentals for a given ticker."""
    console.print(f"[green]Fetching company fundamentals for {ticker.upper()}...[/green]")
    ctx.obj["MARKET_DATA"].get_company_fundamentals(ticker)

@stocks.command()
@click.argument("ticker")
@click.pass_context
def financials(ctx, ticker):
    """Get financial statements (income, balance, cash flow) for a given ticker."""
    console.print(f"[green]Fetching financial statements for {ticker.upper()}...[/green]")
    ctx.obj["MARKET_DATA"].get_financial_statements(ticker)

@stocks.command()
@click.pass_context
def chart(ctx):
    """Display chart for loaded stock."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        console.print("[green]Displaying stock chart...[/green]")
        ctx.obj["CHARTING"].plot_candlestick_chart(current_stock_data, title=f"{current_stock_data.index.name} Candlestick Chart")
    else:
        console.print("[yellow]No stock data loaded to chart. Use ('stocks load <TICKER>') first.[/yellow]")

@cli.group()
def crypto():
    """Cryptocurrency data and analysis commands."""
    pass

@crypto.command()
@click.argument("coin_id")
@click.option("--days", default="30", help="Number of days for historical data.")
@click.pass_context
def chart(ctx, coin_id, days):
    """Get price chart for a cryptocurrency."""
    console.print(f"[green]Fetching price chart for {coin_id}...[/green]")
    df = ctx.obj["CRYPTO_DATA"].get_price_chart(coin_id, days=days)
    if df is not None:
        ctx.obj["CHARTING"].plot_line_chart(df["price"], title=f"{coin_id.upper()} Price Chart", x_label="Date", y_label="Price")

@crypto.command()
@click.option("--per_page", default=10, help="Number of cryptocurrencies to display.")
@click.pass_context
def rankings(ctx, per_page):
    """Get market cap rankings for cryptocurrencies."""
    console.print("[green]Fetching market cap rankings...[/green]")
    ctx.obj["CRYPTO_DATA"].get_market_cap_rankings(per_page=per_page)

@crypto.command()
@click.argument("coin_id")
@click.pass_context
def info(ctx, coin_id):
    """Get detailed information about a cryptocurrency."""
    console.print(f"[green]Fetching information for {coin_id}...[/green]")
    ctx.obj["CRYPTO_DATA"].get_coin_info(coin_id)

@crypto.command()
@click.argument("symbol")
def load(symbol):
    """Load cryptocurrency data for a given symbol."""
    console.print(f"[green]Loading crypto data for {symbol.upper()}...[/green]")
    # TODO: Implement crypto data loading
    console.print(f"[yellow]Crypto data loading for {symbol.upper()} - Not implemented yet[/yellow]")

@cli.group()
def forex():
    """Foreign exchange data commands."""
    pass

@forex.command()
@click.argument("base_currency")
@click.pass_context
def rates(ctx, base_currency):
    """Get live exchange rates for a base currency."""
    console.print(f"[green]Fetching live rates for {base_currency.upper()}...[/green]")
    ctx.obj["FOREX_DATA"].get_live_rates(base_currency)

@forex.command()
@click.argument("base_currency")
@click.argument("target_currency")
@click.argument("date")
@click.pass_context
def history(ctx, base_currency, target_currency, date):
    """Get historical exchange rate for a specific date."""
    console.print(f"[green]Fetching historical rate for {base_currency.upper()}/{target_currency.upper()} on {date}...[/green]")
    ctx.obj["FOREX_DATA"].get_historical_chart(base_currency, target_currency, date)

@cli.group()
def macro():
    """Macroeconomic data commands."""
    pass

@macro.command()
@click.argument("series_id")
@click.option("--start_date", help="Start date (YYYY-MM-DD).")
@click.option("--end_date", help="End date (YYYY-MM-DD).")
@click.pass_context
def fred(ctx, series_id, start_date, end_date):
    """Get data for a FRED series ID."""
    api_key = ctx.obj["CONFIG_MANAGER"].get("fred_api_key")
    if not api_key:
        console.print("[bold red]Error:[/bold red] FRED API key not configured. Use ('config set fred_api_key YOUR_KEY').")
        return
    console.print(f"[green]Fetching FRED series {series_id.upper()}...[/green]")
    ctx.obj["MACRO_DATA"].get_fred_series(series_id, api_key, start_date, end_date)

@macro.command()
@click.option("--start_date", help="Start date (YYYY-MM-DD).")
@click.option("--end_date", help="End date (YYYY-MM-DD).")
@click.pass_context
def inflation(ctx, start_date, end_date):
    """Get US inflation rate."""
    api_key = ctx.obj["CONFIG_MANAGER"].get("fred_api_key")
    if not api_key:
        console.print("[bold red]Error:[/bold red] FRED API key not configured. Use ('config set fred_api_key YOUR_KEY').")
    return ctx.obj["MACRO_DATA"].get_inflation_rate(api_key, start_date, end_date)

@macro.command()
@click.option("--start_date", help="Start date (YYYY-MM-DD).")
@click.option("--end_date", help="End date (YYYY-MM-DD).")
@click.pass_context
def gdp(ctx, start_date, end_date):
    """Get US GDP."""
    api_key = ctx.obj["CONFIG_MANAGER"].get("fred_api_key")
    if not api_key:
        console.print("[bold red]Error:[/bold red] FRED API key not configured. Use ('config set fred_api_key YOUR_KEY').")
    return ctx.obj["MACRO_DATA"].get_gdp(api_key, start_date, end_date)

@macro.command()
@click.option("--start_date", help="Start date (YYYY-MM-DD).")
@click.option("--end_date", help="End date (YYYY-MM-DD).")
@click.pass_context
def interest_rates(ctx, start_date, end_date):
    """Get Federal Funds Rate."""
    api_key = ctx.obj["CONFIG_MANAGER"].get("fred_api_key")
    if not api_key:
        console.print("[bold red]Error:[/bold red] FRED API key not configured. Use ('config set fred_api_key YOUR_KEY').")      
    return ctx.obj["MACRO_DATA"].get_interest_rates(api_key, start_date, end_date)

@macro.command()
@click.option("--start_date", help="Start date (YYYY-MM-DD).")
@click.option("--end_date", help="End date (YYYY-MM-DD).")
@click.pass_context
def unemployment(ctx, start_date, end_date):
    """Get US Unemployment Rate."""
    api_key = ctx.obj["CONFIG_MANAGER"].get("fred_api_key")
    if not api_key:
        console.print("[bold red]Error:[/bold red] FRED API key not configured. Use ('config set fred_api_key YOUR_KEY').")       
    return ctx.obj["MACRO_DATA"].get_unemployment_rate(api_key, start_date, end_date)

@cli.group()
def portfolio():
    """Portfolio management commands."""
    pass

@portfolio.command()
@click.argument("symbol")
@click.argument("quantity", type=float)
@click.argument("purchase_price", type=float)
@click.pass_context
def add(ctx, symbol, quantity, purchase_price):
    """Add a position to the portfolio."""
    ctx.obj["PORTFOLIO_MANAGER"].add_position(symbol, quantity, purchase_price)

@portfolio.command()
@click.pass_context
def view(ctx):
    """View current portfolio."""
    ctx.obj["PORTFOLIO_MANAGER"].view_portfolio()

@portfolio.command()
@click.argument("returns_column")
@click.option("--risk_free_rate", default=0.01, type=float, help="Risk-free rate for Sharpe Ratio calculation.")
@click.pass_context
def sharpe(ctx, returns_column, risk_free_rate):
    """Calculate Sharpe Ratio for loaded data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        if returns_column in current_stock_data.columns:
            ctx.obj["PORTFOLIO_MANAGER"].calculate_sharpe_ratio(current_stock_data[returns_column], risk_free_rate)
        else:
            console.print(f"[bold red]Error:[/bold red] Returns column ('{returns_column}') not found in loaded data.")
    else:
        console.print("[yellow]No data loaded for Sharpe Ratio calculation. Use ('stocks load <TICKER>') first.[/yellow]")

@portfolio.command()
@click.argument("returns_column")
@click.option("--risk_free_rate", default=0.01, type=float, help="Risk-free rate for Sortino Ratio calculation.")
@click.pass_context
def sortino(ctx, returns_column, risk_free_rate):
    """Calculate Sortino Ratio for loaded data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        if returns_column in current_stock_data.columns:
            ctx.obj["PORTFOLIO_MANAGER"].calculate_sortino_ratio(current_stock_data[returns_column], risk_free_rate)
        else:
            console.print(f"[bold red]Error:[/bold red] Returns column ('{returns_column}') not found in loaded data.")
    else:
        console.print("[yellow]No data loaded for Sortino Ratio calculation. Use ('stocks load <TICKER>') first.[/yellow]")

@portfolio.command()
@click.argument("stock_returns_column")
@click.argument("market_returns_column")
@click.pass_context
def beta(ctx, stock_returns_column, market_returns_column):
    """Calculate Beta for loaded data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        if stock_returns_column in current_stock_data.columns and market_returns_column in current_stock_data.columns:
            ctx.obj["PORTFOLIO_MANAGER"].calculate_beta(current_stock_data[stock_returns_column], current_stock_data[market_returns_column])
        else:
            console.print(f"[bold red]Error:[/bold red] One or both returns columns not found in loaded data.")
    else:
        console.print("[yellow]No data loaded for Beta calculation. Use ('stocks load <TICKER>') first.[/yellow]")

@portfolio.command()
@click.pass_context
def backtest(ctx):
    """Run a simple backtesting simulation on loaded data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        console.print("[green]Running backtest...[/green]")
        cumulative_returns = ctx.obj["PORTFOLIO_MANAGER"].run_backtest(current_stock_data.copy(), None) # None for strategy_func as it's hardcoded for now
        if cumulative_returns is not None:
            ctx.obj["CHARTING"].plot_line_chart(cumulative_returns, title="Equity Curve", x_label="Time", y_label="Cumulative Returns")
    else:
        console.print("[yellow]No stock data loaded for backtesting. Use ('stocks load <TICKER>') first.[/yellow]")

@cli.group()
def config():
    """Configuration settings commands."""
    pass

@config.command()
@click.pass_context
def show(ctx):
    """Show current configuration."""
    ctx.obj["CONFIG_MANAGER"].show()

@config.command()
@click.argument("key")
@click.argument("value")
@click.pass_context
def set(ctx, key, value):
    """Set a configuration key-value pair."""
    ctx.obj["CONFIG_MANAGER"].set(key, value)

@config.command()
@click.argument("key")
@click.pass_context
def delete(ctx, key):
    """Delete a configuration key."""
    ctx.obj["CONFIG_MANAGER"].delete(key)

@config.command()
@click.argument("alias")
@click.argument("command", nargs=-1)
@click.pass_context
def alias(ctx, alias, command):
    """Set a command alias."""
    ctx.obj["CONFIG_MANAGER"].set_alias(alias, " ".join(command))

@config.command(name="list_aliases")
@click.pass_context
def list_aliases(ctx):
    """List all configured aliases."""
    ctx.obj["CONFIG_MANAGER"].list_aliases()

@config.command()
@click.argument("alias")
@click.pass_context
def delete_alias(ctx, alias):
    """Delete a command alias."""
    ctx.obj["CONFIG_MANAGER"].delete_alias(alias)

@config.command()
@click.argument("theme_name")
@click.pass_context
def theme(ctx, theme_name):
    """Set the application theme."""
    ctx.obj["CONFIG_MANAGER"].set_theme(theme_name)

@cli.group()
def import_data():
    """Commands for importing data from files."""
    pass

@import_data.command(name='csv')
@click.argument('file_path')
@click.pass_context
def import_csv(ctx, file_path):
    """Import data from a CSV file."""
    try:
        df = ctx.obj["DATA_MANAGER"].load_csv(file_path)
        console.print(f"[green]Successfully loaded CSV from {file_path}. Shape: {df.shape}[/green]")
        console.print(df.head())
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

@import_data.command(name='excel')
@click.argument('file_path')
@click.option('--sheet', default=0, help='Sheet name or index to load from Excel file.')
@click.pass_context
def import_excel(ctx, file_path, sheet):
    """Import data from an Excel file."""
    try:
        df = ctx.obj["DATA_MANAGER"].load_excel(file_path, sheet_name=sheet)
        console.print(f"[green]Successfully loaded Excel from {file_path} (Sheet: {sheet}). Shape: {df.shape}[/green]")
        console.print(df.head())
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

@import_data.command(name='json')
@click.argument('file_path')
@click.pass_context
def import_json(ctx, file_path):
    """Import data from a JSON file."""
    try:
        data = ctx.obj["DATA_MANAGER"].load_json(file_path)
        console.print(f"[green]Successfully loaded JSON from {file_path}.[/green]")
        console.print(data)
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/bold red] {e}")

@cli.group()
def db():
    """Database management commands."""
    pass

@db.command()
@click.argument('table_name')
@click.pass_context
def save(ctx, table_name):
    """Save the currently loaded stock data to the database."""
    global current_stock_data
    if current_stock_data is not None:
        try:
            ctx.obj["DB_MANAGER"].save_dataframe(current_stock_data, table_name)
            console.print(f"[green]Successfully saved data to table ('{table_name}').[/green]")
        except Exception as e:
            console.print(f"[bold red]Error saving to DB:[/bold red] {e}")
    else:
        console.print("[yellow]No stock data loaded to save. Use ('stocks load <TICKER>') first.[/yellow]")

@db.command()
@click.argument('table_name')
@click.pass_context
def load(ctx, table_name):
    """Load data from a database table."""
    global current_stock_data
    try:
        df = ctx.obj["DB_MANAGER"].load_dataframe(table_name)
        if df is not None:
            current_stock_data = df
            console.print(f"[green]Successfully loaded data from table ('{table_name}'). Shape: {df.shape}[/green]")
            console.print(df.head())
        else:
            console.print(f"[yellow]Table ('{table_name}') not found or empty.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error loading from DB:[/bold red] {e}")

@db.command(name='list')
@click.pass_context
def list_tables(ctx):
    """List all tables in the database."""
    try:
        tables = ctx.obj["DB_MANAGER"].list_tables()
        if tables:
            console.print("[green]Available tables:[/green]")
            for table in tables:
                console.print(f"- {table}")
        else:
            console.print("[yellow]No tables found in the database.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error listing tables:[/bold red] {e}")

@cli.group()
def analyze():
    """Quantitative analysis and technical indicators commands."""
    pass

@analyze.command()
@click.pass_context
def ta(ctx):
    """Calculate and display technical indicators for the loaded stock data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        console.print("[green]Calculating technical indicators...[/green]")
        df_with_ta = ctx.obj["ANALYTICS"].calculate_technical_indicators(current_stock_data.copy())
        if df_with_ta is not None:
            ctx.obj["ANALYTICS"].display_technical_indicators(df_with_ta)
    else:
        console.print("[yellow]No stock data loaded for technical analysis. Use ('stocks load <TICKER>') first.[/yellow]")

@analyze.command()
@click.option("--columns", multiple=True, help="Columns to calculate correlations for (e.g., --columns Open --columns Close).")
@click.pass_context
def correlation(ctx, columns):
    """Calculate and display correlation matrix for the loaded stock data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        console.print("[green]Calculating correlations...[/green]")
        ctx.obj["ANALYTICS"].calculate_correlations(current_stock_data, list(columns) if columns else None)
    else:
        console.print("[yellow]No stock data loaded for correlation analysis. Use ('stocks load <TICKER>') first.[/yellow]")

@analyze.command()
@click.option("--column", default="Close", help="Column to calculate volatility for.")
@click.option("--window", default=20, type=int, help="Rolling window for volatility calculation.")
@click.pass_context
def volatility(ctx, column, window):
    """Calculate and display rolling volatility for the loaded stock data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        console.print("[green]Calculating volatility...[/green]")
        ctx.obj["ANALYTICS"].calculate_volatility(current_stock_data, column, window)
    else:
        console.print("[yellow]No stock data loaded for volatility analysis. Use ('stocks load <TICKER>') first.[/yellow]")

@analyze.command()
@click.argument("dependent_var")
@click.argument("independent_vars", nargs=-1)
@click.pass_context
def regression(ctx, dependent_var, independent_vars):
    """Perform linear regression analysis on the loaded stock data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        if not independent_vars:
            console.print("[bold red]Error:[/bold red] Please provide at least one independent variable for regression.")
            return
        console.print("[green]Performing regression analysis...[/green]")
        ctx.obj["ANALYTICS"].perform_regression_analysis(current_stock_data, dependent_var, list(independent_vars))
    else:
        console.print("[yellow]No stock data loaded for regression analysis. Use ('stocks load <TICKER>') first.[/yellow]")

@cli.group()
def trade():
    """Trading simulation and order management commands."""
    pass

@trade.command()
@click.argument("symbol")
@click.argument("quantity", type=float)
@click.argument("price", type=float)
@click.pass_context
def buy(ctx, symbol, quantity, price):
    """Simulate a buy order."""
    ctx.obj["TRADING_SIMULATOR"].buy(symbol, quantity, price)

@trade.command()
@click.argument("symbol")
@click.argument("quantity", type=float)
@click.argument("price", type=float)
@click.pass_context
def sell(ctx, symbol, quantity, price):
    """Simulate a sell order."""
    ctx.obj["TRADING_SIMULATOR"].sell(symbol, quantity, price)

@trade.command(name='balance')
@click.pass_context
def view_balance(ctx):
    """View current cash balance."""
    ctx.obj["TRADING_SIMULATOR"].view_balance()

@trade.command(name='positions')
@click.pass_context
def view_positions(ctx):
    """View current open positions."""
    ctx.obj["TRADING_SIMULATOR"].view_positions()

@trade.command(name='history')
@click.pass_context
def view_trade_history(ctx):
    """View trade history."""
    ctx.obj["TRADING_SIMULATOR"].view_trade_history()

@trade.command()
@click.argument("api_key")
@click.argument("secret_key")
@click.pass_context
def connect_exchange(ctx, api_key, secret_key):
    """Connect to a real exchange API (placeholder)."""
    ctx.obj["TRADING_SIMULATOR"].connect_exchange_api(api_key, secret_key)

@trade.command()
@click.argument("order_type")
@click.argument("symbol")
@click.argument("quantity", type=float)
@click.option("--price", type=float, help="Price for limit orders.")
@click.pass_context
def place_order(ctx, order_type, symbol, quantity, price):
    """Place a real order via exchange API (placeholder)."""
    ctx.obj["TRADING_SIMULATOR"].place_real_order(order_type, symbol, quantity, price)

@cli.group()
def report():
    """Reporting and export features."""
    pass

@report.command(name='csv')
@click.argument('filename')
@click.pass_context
def export_csv(ctx, filename):
    """Export currently loaded stock data to a CSV file."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        ctx.obj["REPORTING"].export_dataframe_to_csv(current_stock_data, filename)
    else:
        console.print("[yellow]No stock data loaded to export. Use ('stocks load <TICKER>') first.[/yellow]")

@report.command(name='excel')
@click.argument('filename')
@click.pass_context
def export_excel(ctx, filename):
    """Export currently loaded stock data to an Excel file."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        ctx.obj["REPORTING"].export_dataframe_to_excel(current_stock_data, filename)
    else:
        console.print("[yellow]No stock data loaded to export. Use ('stocks load <TICKER>') first.[/yellow]")

@report.command(name='pdf')
@click.argument('filename')
@click.option('--title', default='Quant Report', help='Title of the PDF report.')
@click.pass_context
def generate_pdf(ctx, filename, title):
    """Generate a PDF report from loaded stock data."""
    global current_stock_data
    if current_stock_data is not None and not current_stock_data.empty:
        content = {
            "Stock Data": current_stock_data.tail(10), # Example: last 10 rows
            "Trade History": ctx.obj["TRADING_SIMULATOR"].trade_history.tail(10) # Example: last 10 trades
        }
        ctx.obj["REPORTING"].generate_pdf_report(title, content, filename)
    else:
        console.print("[yellow]No stock data loaded for PDF report. Use ('stocks load <TICKER>') first.[/yellow]")

@report.command(name='email')
@click.argument('recipient')
@click.argument('subject')
@click.argument('body')
@click.pass_context
def send_email(ctx, recipient, subject, body):
    """Send an email alert."""
    ctx.obj["REPORTING"].send_email_alert(recipient, subject, body)

@report.command(name='notify')
@click.argument('message')
@click.option('--style', default='green', help='Style for the notification (e.g., green, red, yellow).')
@click.pass_context
def send_notification(ctx, message, style):
    """Send a terminal notification."""
    ctx.obj["REPORTING"].send_terminal_notification(message, style)

@cli.group()
def security():
    """Security features (encryption, authentication)."""
    pass

@security.command()
@click.argument("data")
@click.pass_context
def encrypt(ctx, data):
    """Encrypt a string of data."""
    encrypted_data = ctx.obj["SECURITY_MANAGER"].encrypt_data(data)
    if encrypted_data:
        console.print(f"[green]Encrypted data: {encrypted_data}[/green]")

@security.command()
@click.argument("encrypted_data")
@click.pass_context
def decrypt(ctx, encrypted_data):
    """Decrypt a string of data."""
    decrypted_data = ctx.obj["SECURITY_MANAGER"].decrypt_data(encrypted_data)
    if decrypted_data:
        console.print(f"[green]Decrypted data: {decrypted_data}[/green]")

@security.command()
@click.argument("input_file")
@click.argument("output_file")
@click.pass_context
def encrypt_file(ctx, input_file, output_file):
    """Encrypt the content of a file."""
    ctx.obj["SECURITY_MANAGER"].encrypt_file(input_file, output_file)

@security.command()
@click.argument("input_file")
@click.argument("output_file")
@click.pass_context
def decrypt_file(ctx, input_file, output_file):
    """Decrypt the content of an encrypted file."""
    ctx.obj["SECURITY_MANAGER"].decrypt_file(input_file, output_file)

@security.command()
@click.argument("username")
@click.argument("password")
@click.pass_context
def setup_auth(ctx, username, password):
    """Set up user authentication (placeholder)."""
    ctx.obj["SECURITY_MANAGER"].setup_authentication(username, password)

@security.command()
@click.argument("username")
@click.argument("password")
@click.pass_context
def verify_auth(ctx, username, password):
    """Verify user authentication (placeholder)."""
    ctx.obj["SECURITY_MANAGER"].verify_authentication(username, password)

@security.command()
@click.pass_context
def enable_sandbox(ctx):
    """Enable sandbox mode (placeholder)."""
    ctx.obj["SECURITY_MANAGER"].enable_sandbox_mode()

@security.command()
@click.pass_context
def disable_sandbox(ctx):
    """Disable sandbox mode (placeholder)."""
    ctx.obj["SECURITY_MANAGER"].disable_sandbox_mode()

if __name__ == '__main__':
    while True:
        try:
            text = session.prompt('FinancialWizard> ', completer=command_completer)
            # Check for aliases before processing
            alias_command = config_manager.get_alias(text.split()[0])
            if alias_command:
                text = alias_command + " " + " ".join(text.split()[1:])

            if text.lower() == 'exit':
                break
            
            args = text.split()
            if args:
                try:
                    cli.main(args=args, standalone_mode=False)
                except SystemExit as e:
                    if e.code != 0:
                        console.print(f"[bold red]Error:[/bold red] Invalid command or arguments.")
            
        except EOFError:
            break # Ctrl-D pressed
        except KeyboardInterrupt:
            continue # Ctrl-C pressed, continue prompt



