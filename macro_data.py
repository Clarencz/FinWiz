import requests
from rich.console import Console
from rich.table import Table

console = Console()

class MacroData:
    def __init__(self):
        # FRED API key is required for most endpoints. Store it in config.
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"

    def get_fred_series(self, series_id, api_key, observation_start=None, observation_end=None):
        """Get observations for a FRED series."""
        if not api_key:
            console.print("[bold red]Error:[/bold red] FRED API key not configured. Use 'config set fred_api_key YOUR_KEY'.")
            return None

        try:
            params = {
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
            }
            if observation_start:
                params["observation_start"] = observation_start
            if observation_end:
                params["observation_end"] = observation_end

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data and "observations" in data:
                table = Table(title=f"[bold blue]FRED Series: {series_id.upper()}[/bold blue]")
                table.add_column("Date", style="cyan")
                table.add_column("Value", style="magenta")

                for obs in data["observations"]:
                    table.add_row(obs["date"], obs["value"])
                
                console.print(table)
                return data["observations"]
            else:
                console.print(f"[yellow]No data found for FRED series {series_id.upper()}.[/yellow]")
                return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching FRED series {series_id}:[/bold red] {e}")
            return None

    def get_inflation_rate(self, api_key, start_date=None, end_date=None):
        """Get US inflation rate (CPIAUCSL series)."""
        console.print("[green]Fetching US Inflation Rate (CPIAUCSL)...[/green]")
        return self.get_fred_series("CPIAUCSL", api_key, start_date, end_date)

    def get_gdp(self, api_key, start_date=None, end_date=None):
        """Get US GDP (GDP series).""" 
        console.print("[green]Fetching US GDP (GDP)...[/green]")
        return self.get_fred_series("GDP", api_key, start_date, end_date)

    def get_interest_rates(self, api_key, start_date=None, end_date=None):
        """Get Federal Funds Rate (FEDFUNDS series)."""
        console.print("[green]Fetching Federal Funds Rate (FEDFUNDS)...[/green]")
        return self.get_fred_series("FEDFUNDS", api_key, start_date, end_date)

    def get_unemployment_rate(self, api_key, start_date=None, end_date=None):
        """Get US Unemployment Rate (UNRATE series)."""
        console.print("[green]Fetching US Unemployment Rate (UNRATE)...[/green]")
        return self.get_fred_series("UNRATE", api_key, start_date, end_date)


