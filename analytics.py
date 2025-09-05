import pandas as pd
import pandas_ta as ta
from rich.console import Console
from rich.table import Table

console = Console()

class Analytics:
    def __init__(self):
        pass

    def calculate_technical_indicators(self, df):
        """Calculate various technical indicators for the given DataFrame."""
        if 'Close' not in df.columns:
            console.print("[bold red]Error:[/bold red] DataFrame must contain a 'Close' column for technical indicator calculation.")
            return None

        # Moving Averages
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['EMA_20'] = ta.ema(df['Close'], length=20)
        df['WMA_20'] = ta.wma(df['Close'], length=20)

        # RSI
        df['RSI'] = ta.rsi(df['Close'])

        # MACD
        macd = ta.macd(df['Close'])
        if macd is not None and not macd.empty:
            df = pd.concat([df, macd], axis=1)

        # Bollinger Bands
        bbands = ta.bbands(df['Close'])
        if bbands is not None and not bbands.empty:
            df = pd.concat([df, bbands], axis=1)

        # Support and Resistance (simplified - typically requires more complex logic)
        # For demonstration, we'll use rolling min/max as a very basic proxy
        df['Support'] = df['Low'].rolling(window=10).min()
        df['Resistance'] = df['High'].rolling(window=10).max()

        console.print("[green]Technical indicators calculated.[/green]")
        return df

    def display_technical_indicators(self, df):
        """Display a summary of technical indicators."""
        if df is None or df.empty:
            console.print("[yellow]No data to display technical indicators.[/yellow]")
            return

        table = Table(title="[bold blue]Technical Indicators Summary[/bold blue]")
        table.add_column("Date", style="cyan")
        table.add_column("Close", style="magenta", justify="right")
        table.add_column("SMA_20", justify="right")
        table.add_column("RSI", justify="right")
        table.add_column("MACD", justify="right")
        table.add_column("Signal", justify="right")
        table.add_column("Hist", justify="right")
        table.add_column("BBL", justify="right")
        table.add_column("BBM", justify="right")
        table.add_column("BBU", justify="right")

        # Display last few rows of indicators
        for index, row in df.tail(10).iterrows():
            table.add_row(
                str(index.date()),
                f"{row['Close']:.2f}",
                f"{row.get('SMA_20', float('nan')):.2f}",
                f"{row.get('RSI', float('nan')):.2f}",
                f"{row.get('MACD_12_26_9', float('nan')):.2f}",
                f"{row.get('MACDH_12_26_9', float('nan')):.2f}",
                f"{row.get('MACDS_12_26_9', float('nan')):.2f}",
                f"{row.get('BBL_5_2.0', float('nan')):.2f}",
                f"{row.get('BBM_5_2.0', float('nan')):.2f}",
                f"{row.get('BBU_5_2.0', float('nan')):.2f}"
            )
        console.print(table)

    def calculate_correlations(self, df, columns=None):
        """Calculate and display correlation matrix."""
        if df.empty:
            console.print("[yellow]No data to calculate correlations.[/yellow]")
            return

        if columns:
            df_corr = df[columns]
        else:
            df_corr = df.select_dtypes(include=[float, int]) # Select only numeric columns

        correlation_matrix = df_corr.corr()
        console.print("[green]Correlation Matrix:[/green]")
        console.print(correlation_matrix)
        return correlation_matrix

    def calculate_volatility(self, df, column='Close', window=20):
        """Calculate and display rolling volatility."""
        if df.empty or column not in df.columns:
            console.print(f"[yellow]No data or '{column}' column not found to calculate volatility.[/yellow]")
            return

        returns = df[column].pct_change().dropna()
        rolling_volatility = returns.rolling(window=window).std() * (252**0.5) # Annualized volatility

        console.print(f"[green]Rolling {window}-day Annualized Volatility for {column}:[/green]")
        console.print(rolling_volatility.tail())
        return rolling_volatility

    def perform_regression_analysis(self, df, dependent_var, independent_vars):
        """Perform linear regression analysis."""
        try:
            import statsmodels.api as sm
        except ImportError:
            console.print("[bold red]Error:[/bold red] statsmodels library not found. Please install it: pip install statsmodels")
            return

        if df.empty or dependent_var not in df.columns or not all(col in df.columns for col in independent_vars):
            console.print("[yellow]Missing data or columns for regression analysis.[/yellow]")
            return

        X = df[independent_vars]
        y = df[dependent_var]

        # Add a constant to the independent variables for intercept calculation
        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit()

        console.print("[green]Regression Analysis Results:[/green]")
        console.print(model.summary())
        return model


