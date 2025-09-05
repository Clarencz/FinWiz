import requests
from rich.console import Console
from rich.table import Table

console = Console()

class ForexData:
    def __init__(self):
        # Using a free API for demonstration. Real applications would need a more robust solution.
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_live_rates(self, base_currency="USD"):
        """Get live exchange rates for a base currency."""
        try:
            url = f"{self.base_url}{base_currency}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and "rates" in data:
                table = Table(title=f"[bold blue]Live Exchange Rates (Base: {base_currency.upper()})[/bold blue]")
                table.add_column("Currency", style="cyan")
                table.add_column("Rate", style="magenta")
                
                for currency, rate in data["rates"].items():
                    table.add_row(currency, f"{rate:.4f}")
                
                console.print(table)
                return data["rates"]
            else:
                console.print(f"[yellow]No live rates found for {base_currency.upper()}.[/yellow]")
                return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching live rates for {base_currency}:[/bold red] {e}")
            return None

    def get_historical_chart(self, base_currency, target_currency, date):
        """Get historical exchange rate for a specific date."""
        # This free API only provides latest rates, not historical data directly.
        # For historical charts, a different API or data source would be needed.
        console.print("[yellow]Historical charts are not supported by the current free API.[/yellow]")
        console.print("[yellow]Please consider integrating with a more comprehensive Forex API for this feature.[/yellow]")
        return None


