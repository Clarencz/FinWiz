import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()

class PortfolioManager:
    def __init__(self):
        self.portfolio = pd.DataFrame(columns=["Symbol", "Quantity", "PurchasePrice", "CurrentPrice", "Value", "GainLoss", "GainLossPct"])

    def add_position(self, symbol, quantity, purchase_price):
        """Add a position to the portfolio."""
        new_position = pd.DataFrame([{
            "Symbol": symbol.upper(),
            "Quantity": quantity,
            "PurchasePrice": purchase_price,
            "CurrentPrice": 0, # Will be updated later
            "Value": 0,
            "GainLoss": 0,
            "GainLossPct": 0
        }])
        self.portfolio = pd.concat([self.portfolio, new_position], ignore_index=True)
        console.print(f"[green]Added {quantity} shares of {symbol.upper()} to portfolio.[/green]")

    def update_prices(self, market_data_source):
        """Update current prices for all holdings in the portfolio."""
        console.print("[green]Updating portfolio prices...[/green]")
        for index, row in self.portfolio.iterrows():
            ticker = row["Symbol"]
            # This is a placeholder. In a real app, you'd fetch live data.
            # For now, let's simulate a price update.
            simulated_current_price = row["PurchasePrice"] * (1 + np.random.uniform(-0.05, 0.05))
            self.portfolio.loc[index, "CurrentPrice"] = simulated_current_price
            self.portfolio.loc[index, "Value"] = row["Quantity"] * simulated_current_price
            self.portfolio.loc[index, "GainLoss"] = (simulated_current_price - row["PurchasePrice"]) * row["Quantity"]
            self.portfolio.loc[index, "GainLossPct"] = ((simulated_current_price - row["PurchasePrice"]) / row["PurchasePrice"]) * 100
        console.print("[green]Portfolio prices updated.[/green]")

    def view_portfolio(self):
        """Display the current portfolio."""
        if self.portfolio.empty:
            console.print("[yellow]Portfolio is empty. Add some positions first.[/yellow]")
            return

        self.update_prices(None) # Update prices before viewing

        table = Table(title="[bold blue]Current Portfolio[/bold blue]")
        table.add_column("Symbol", style="cyan")
        table.add_column("Quantity", style="magenta", justify="right")
        table.add_column("Purchase Price", style="yellow", justify="right")
        table.add_column("Current Price", style="green", justify="right")
        table.add_column("Value", style="blue", justify="right")
        table.add_column("Gain/Loss", justify="right")
        table.add_column("Gain/Loss %", justify="right")

        total_value = 0
        total_gain_loss = 0

        for index, row in self.portfolio.iterrows():
            gain_loss_color = "green" if row["GainLoss"] >= 0 else "red"
            gain_loss_pct_color = "green" if row["GainLossPct"] >= 0 else "red"
            
            table.add_row(
                row["Symbol"],
                f"{row['Quantity']:.2f}",
                f"{row['PurchasePrice']:.2f}",
                f"{row['CurrentPrice']:.2f}",
                f"{row['Value']:.2f}",
                f"[{gain_loss_color}]{row['GainLoss']:.2f}[/{gain_loss_color}]",
                f"[{gain_loss_pct_color}]{row['GainLossPct']:.2f}%[/{gain_loss_pct_color}]"
            )
            total_value += row["Value"]
            total_gain_loss += row["GainLoss"]

        console.print(table)
        console.print(f"[bold]Total Portfolio Value:[/bold] [green]${total_value:.2f}[/green]")
        total_gain_loss_color = "green" if total_gain_loss >= 0 else "red"
        console.print(f"[bold]Total Portfolio Gain/Loss:[/bold] [{total_gain_loss_color}]${total_gain_loss:.2f}[/{total_gain_loss_color}]")

    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.01):
        """Calculate Sharpe Ratio."""
        if returns.empty:
            console.print("[yellow]No returns data to calculate Sharpe Ratio.[/yellow]")
            return None
        
        excess_returns = returns - risk_free_rate
        sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
        console.print(f"[green]Sharpe Ratio: {sharpe_ratio:.4f}[/green]")
        return sharpe_ratio

    def calculate_sortino_ratio(self, returns, risk_free_rate=0.01):
        """Calculate Sortino Ratio."""
        if returns.empty:
            console.print("[yellow]No returns data to calculate Sortino Ratio.[/yellow]")
            return None

        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns)
        
        if downside_std == 0:
            console.print("[yellow]No downside deviation to calculate Sortino Ratio.[/yellow]")
            return None

        sortino_ratio = (np.mean(returns) - risk_free_rate) / downside_std
        console.print(f"[green]Sortino Ratio: {sortino_ratio:.4f}[/green]")
        return sortino_ratio

    def calculate_beta(self, stock_returns, market_returns):
        """Calculate Beta."""
        if stock_returns.empty or market_returns.empty:
            console.print("[yellow]No returns data to calculate Beta.[/yellow]")
            return None

        covariance = stock_returns.cov(market_returns)
        market_variance = market_returns.var()
        
        if market_variance == 0:
            console.print("[yellow]Market variance is zero, cannot calculate Beta.[/yellow]")
            return None

        beta = covariance / market_variance
        console.print(f"[green]Beta: {beta:.4f}[/green]")
        return beta

    def run_backtest(self, data, strategy_func):
        """Run a simple backtesting simulation."""
        if data.empty:
            console.print("[yellow]No data to run backtest.[/yellow]")
            return None

        console.print("[green]Running backtest...[/green]")
        # This is a simplified backtesting framework.
        # A real backtesting engine would be much more complex.
        
        # Example: Simple Moving Average Crossover Strategy
        # Buy when SMA(10) crosses above SMA(30), Sell when SMA(10) crosses below SMA(30)
        
        # Ensure data has 'Close' prices
        if 'Close' not in data.columns:
            console.print("[bold red]Error:[/bold red] Data must contain a 'Close' column for backtesting.")
            return None

        # Calculate SMAs
        data['SMA10'] = data['Close'].rolling(window=10).mean()
        data['SMA30'] = data['Close'].rolling(window=30).mean()

        # Generate signals
        data['Signal'] = 0
        data['Signal'][data['SMA10'] > data['SMA30']] = 1  # Buy signal
        data['Signal'][data['SMA10'] < data['SMA30']] = -1 # Sell signal

        # Calculate positions
        data['Position'] = data['Signal'].shift(1)

        # Calculate daily returns
        data['StrategyReturns'] = data['Position'] * data['Close'].pct_change()

        # Calculate cumulative returns
        data['CumulativeReturns'] = (1 + data['StrategyReturns']).cumprod()

        console.print("[green]Backtest completed. Cumulative Returns:[/green]")
        console.print(data['CumulativeReturns'].tail())
        return data['CumulativeReturns']

    def plot_equity_curve(self, cumulative_returns, title="Equity Curve"):
        """Plot the equity curve using plotext."""
        if cumulative_returns is None or cumulative_returns.empty:
            console.print("[yellow]No cumulative returns data to plot equity curve.[/yellow]")
            return

        plt.clear_figure()
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Cumulative Returns")

        x = list(range(len(cumulative_returns)))
        y = cumulative_returns.values

        plt.plot(x, y, color="green")
        plt.show()
        console.print("[green]Equity curve displayed.[/green]")




