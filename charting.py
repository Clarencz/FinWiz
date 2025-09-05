import plotext as plt
from rich.console import Console
from rich.table import Table
from rich.text import Text
import pandas as pd

console = Console()

class Charting:
    def __init__(self):
        pass

    def plot_line_chart(self, data, title="Line Chart", x_label="Date", y_label="Value", color="blue"):
        """Plots a simple line chart using plotext."""
        if data.empty:
            console.print("[yellow]No data to plot for line chart.[/yellow]")
            return

        plt.clear_figure()
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        
        # Assuming data is a pandas Series or DataFrame with a single column for values
        # and index for x-axis (e.g., dates)
        x = list(range(len(data)))
        y = data.values.flatten() if isinstance(data, pd.DataFrame) else data.values

        plt.plot(x, y, color=color)
        plt.show()
        console.print("[green]Line chart displayed.[/green]")

    def plot_candlestick_chart(self, ohlcv_data, title="Candlestick Chart"):
        """Plots a candlestick chart using plotext."""
        if ohlcv_data.empty or not all(col in ohlcv_data.columns for col in ["Open", "High", "Low", "Close"]):
            console.print("[yellow]Invalid OHLCV data for candlestick chart. Requires Open, High, Low, Close columns.[/yellow]")
            return

        plt.clear_figure()
        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Price")

        # plotext expects lists for OHLCV
        dates = list(range(len(ohlcv_data)))
        opens = ohlcv_data["Open"].tolist()
        highs = ohlcv_data["High"].tolist()
        lows = ohlcv_data["Low"].tolist()
        closes = ohlcv_data["Close"].tolist()

        plt.candlestick(dates, opens, closes, highs, lows)
        plt.show()
        console.print("[green]Candlestick chart displayed.[/green]")

    def display_color_coded_table(self, df, title="Data Table"):
        """Displays a pandas DataFrame as a rich table with color-coded gain/loss for numeric columns."""
        if df.empty:
            console.print("[yellow]No data to display in table.[/yellow]")
            return

        table = Table(title=title, show_lines=True)

        # Add columns
        for col in df.columns:
            table.add_column(str(col), justify="right", style="cyan")

        # Add rows with color coding for numeric changes (simple gain/loss)
        for index, row in df.iterrows():
            row_data = []
            for col in df.columns:
                value = row[col]
                if pd.api.types.is_numeric_dtype(df[col]) and len(df[col]) > 1:
                    # Simple logic: if current value > previous value, it's a gain (green), else loss (red)
                    # This is a very basic example, more sophisticated logic would be needed for real gain/loss
                    try:
                        prev_value = df[col].iloc[df.index.get_loc(index) - 1]
                        if value > prev_value:
                            row_data.append(Text(f"{value:.2f}", style="green"))
                        elif value < prev_value:
                            row_data.append(Text(f"{value:.2f}", style="red"))
                        else:
                            row_data.append(str(value))
                    except IndexError:
                        row_data.append(str(value)) # First row has no previous value
                else:
                    row_data.append(str(value))
            table.add_row(*row_data)
        
        console.print(table)

    def display_heatmap(self, data, title="Heatmap"):
        """Displays a simple text-based heatmap (conceptual)."""
        console.print(f"[bold blue]{title}[/bold blue]")
        console.print("[yellow]Heatmap visualization is complex in pure text. This is a placeholder.[/yellow]")
        console.print("[yellow]Consider using external libraries like matplotlib for graphical heatmaps.[/yellow]")
        # A very basic text representation
        if not data.empty:
            console.print(data.applymap(lambda x: f"[green]{x:.2f}[/green]" if x > 0 else f"[red]{x:.2f}[/red]").to_string())
        else:
            console.print("[yellow]No data to display for heatmap.[/yellow]")


