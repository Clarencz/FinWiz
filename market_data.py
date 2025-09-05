import yfinance as yf
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

class MarketData:
    def __init__(self):
        pass

    def get_quote_snapshot(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if info:
                table = Table(title=f"[bold blue]{ticker.upper()} Quote Snapshot[/bold blue]")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="magenta")

                metrics = {
                    "Current Price": info.get("currentPrice"),
                    "Open": info.get("open"),
                    "High": info.get("dayHigh"),
                    "Low": info.get("dayLow"),
                    "Previous Close": info.get("previousClose"),
                    "Volume": info.get("volume"),
                    "Market Cap": info.get("marketCap"),
                    "PE Ratio": info.get("trailingPE"),
                    "Forward PE": info.get("forwardPE"),
                    "Dividend Yield": info.get("dividendYield"),
                    "Beta": info.get("beta"),
                    "52 Week High": info.get("fiftyTwoWeekHigh"),
                    "52 Week Low": info.get("fiftyTwoWeekLow"),
                }

                for metric, value in metrics.items():
                    if value is not None:
                        if isinstance(value, (int, float)):
                            if "Price" in metric or "High" in metric or "Low" in metric or "Close" in metric:
                                table.add_row(metric, f"{value:.2f}")
                            elif "Yield" in metric:
                                table.add_row(metric, f"{value:.2%}")
                            elif "Volume" in metric or "Market Cap" in metric:
                                table.add_row(metric, f"{value:,}")
                            else:
                                table.add_row(metric, str(value))
                        else:
                            table.add_row(metric, str(value))
                console.print(table)
                return info
            else:
                console.print(f"[bold red]Error:[/bold red] Could not retrieve quote snapshot for {ticker.upper()}.")
                return None
        except Exception as e:
            console.print(f"[bold red]Error fetching quote snapshot for {ticker}:[/bold red] {e}")
            return None

    def get_ohlcv_history(self, ticker, period="1y", interval="1d"):
        try:
            data = yf.download(ticker, period=period, interval=interval)
            if data.empty:
                console.print(f"[yellow]No OHLCV data found for {ticker.upper()} with period {period} and interval {interval}.[/yellow]")
                return None
            console.print(f"[green]OHLCV history for {ticker.upper()} ({period}, {interval}):[/green]")
            console.print(data.tail())
            return data
        except Exception as e:
            console.print(f"[bold red]Error fetching OHLCV history for {ticker}:[/bold red] {e}")
            return None

    def get_company_fundamentals(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if info:
                console.print(f"[bold blue]{ticker.upper()} Company Fundamentals:[/bold blue]")
                fundamentals = {
                    "Sector": info.get("sector"),
                    "Industry": info.get("industry"),
                    "Full Time Employees": info.get("fullTimeEmployees"),
                    "Business Summary": info.get("longBusinessSummary"),
                }
                for key, value in fundamentals.items():
                    if value:
                        console.print(f"[cyan]{key}:[/cyan] {value}")
                return info
            else:
                console.print(f"[bold red]Error:[/bold red] Could not retrieve company fundamentals for {ticker.upper()}.")
                return None
        except Exception as e:
            console.print(f"[bold red]Error fetching company fundamentals for {ticker}:[/bold red] {e}")
            return None

    def get_financial_statements(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            console.print(f"[bold blue]{ticker.upper()} Financial Statements:[/bold blue]")

            # Income Statement
            income_stmt = stock.financials
            if not income_stmt.empty:
                console.print("[green]Income Statement:[/green]")
                console.print(income_stmt.T)
            else:
                console.print("[yellow]No Income Statement available.[/yellow]")

            # Balance Sheet
            balance_sheet = stock.balance_sheet
            if not balance_sheet.empty:
                console.print("[green]Balance Sheet:[/green]")
                console.print(balance_sheet.T)
            else:
                console.print("[yellow]No Balance Sheet available.[/yellow]")

            # Cash Flow
            cash_flow = stock.cashflow
            if not cash_flow.empty:
                console.print("[green]Cash Flow:[/green]")
                console.print(cash_flow.T)
            else:
                console.print("[yellow]No Cash Flow available.[/yellow]")

            return {
                "income_statement": income_stmt,
                "balance_sheet": balance_sheet,
                "cash_flow": cash_flow
            }
        except Exception as e:
            console.print(f"[bold red]Error fetching financial statements for {ticker}:[/bold red] {e}")
            return None


