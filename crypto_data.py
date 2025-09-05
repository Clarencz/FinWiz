import requests
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

class CryptoData:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_price_chart(self, coin_id, vs_currency="usd", days="30"):
        """Get historical market data for a cryptocurrency."""
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {"vs_currency": vs_currency, "days": days}
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            if "prices" in data:
                prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
                prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")
                console.print(f"[green]Price chart for {coin_id.upper()} ({days} days):[/green]")
                console.print(prices.tail())
                return prices
            else:
                console.print(f"[yellow]No price data found for {coin_id}.[/yellow]")
                return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching price chart for {coin_id}:[/bold red] {e}")
            return None

    def get_market_cap_rankings(self, vs_currency="usd", per_page=10, page=1):
        """Get market cap rankings for cryptocurrencies."""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": vs_currency,
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": page,
                "sparkline": False
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data:
                table = Table(title=f"[bold blue]Top {per_page} Cryptocurrencies by Market Cap[/bold blue]")
                table.add_column("Rank", style="cyan")
                table.add_column("Name", style="magenta")
                table.add_column("Symbol", style="yellow")
                table.add_column("Price", style="green")
                table.add_column("Market Cap", style="blue")
                table.add_column("24h Change", style="red")
                
                for coin in data:
                    rank = str(coin.get("market_cap_rank", "N/A"))
                    name = coin.get("name", "N/A")
                    symbol = coin.get("symbol", "").upper()
                    price = f"${coin.get('current_price', 0):,.2f}"
                    market_cap = f"${coin.get('market_cap', 0):,}"
                    change_24h = coin.get("price_change_percentage_24h", 0)
                    change_color = "green" if change_24h >= 0 else "red"
                    change_str = f"[{change_color}]{change_24h:.2f}%[/{change_color}]"
                    
                    table.add_row(rank, name, symbol, price, market_cap, change_str)
                
                console.print(table)
                return data
            else:
                console.print("[yellow]No market cap data found.[/yellow]")
                return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching market cap rankings:[/bold red] {e}")
            return None

    def get_coin_info(self, coin_id):
        """Get detailed information about a specific cryptocurrency."""
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data:
                table = Table(title=f"[bold blue]{data.get('name', coin_id).upper()} Information[/bold blue]")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="magenta")
                
                metrics = {
                    "Name": data.get("name"),
                    "Symbol": data.get("symbol", "").upper(),
                    "Current Price (USD)": f"${data.get('market_data', {}).get('current_price', {}).get('usd', 0):,.2f}",
                    "Market Cap (USD)": f"${data.get('market_data', {}).get('market_cap', {}).get('usd', 0):,}",
                    "Total Volume (USD)": f"${data.get('market_data', {}).get('total_volume', {}).get('usd', 0):,}",
                    "24h Change": f"{data.get('market_data', {}).get('price_change_percentage_24h', 0):.2f}%",
                    "7d Change": f"{data.get('market_data', {}).get('price_change_percentage_7d', 0):.2f}%",
                    "All Time High (USD)": f"${data.get('market_data', {}).get('ath', {}).get('usd', 0):,.2f}",
                    "All Time Low (USD)": f"${data.get('market_data', {}).get('atl', {}).get('usd', 0):,.2f}",
                    "Circulating Supply": f"{data.get('market_data', {}).get('circulating_supply', 0):,}",
                    "Total Supply": f"{data.get('market_data', {}).get('total_supply', 0):,}",
                    "Max Supply": f"{data.get('market_data', {}).get('max_supply', 0):,}" if data.get('market_data', {}).get('max_supply') else "N/A",
                }
                
                for metric, value in metrics.items():
                    table.add_row(metric, str(value))
                
                console.print(table)
                
                # Display description if available
                description = data.get("description", {}).get("en", "")
                if description:
                    console.print(f"\n[bold blue]Description:[/bold blue]\n{description[:500]}...")
                
                return data
            else:
                console.print(f"[yellow]No information found for {coin_id}.[/yellow]")
                return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Error fetching coin information for {coin_id}:[/bold red] {e}")
            return None

