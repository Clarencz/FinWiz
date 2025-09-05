import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

class TradingSimulator:
    def __init__(self, initial_balance=100000.0):
        self.balance = initial_balance
        self.positions = {}
        self.trade_history = pd.DataFrame(columns=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Value", "Status"])
        self.order_id_counter = 0

    def _generate_order_id(self):
        self.order_id_counter += 1
        return f"ORD-{self.order_id_counter:05d}"

    def _record_trade(self, order_id, trade_type, symbol, quantity, price, value, status="Filled"):
        new_trade = pd.DataFrame([{
            "Timestamp": pd.Timestamp.now(),
            "OrderID": order_id,
            "Type": trade_type,
            "Symbol": symbol.upper(),
            "Quantity": quantity,
            "Price": price,
            "Value": value,
            "Status": status
        }])
        self.trade_history = pd.concat([self.trade_history, new_trade], ignore_index=True)

    def buy(self, symbol, quantity, price):
        """Simulate a buy order."""
        cost = quantity * price
        if cost > self.balance:
            console.print(f"[bold red]Error:[/bold red] Insufficient balance to buy {quantity} of {symbol}. Cost: ${cost:.2f}, Available: ${self.balance:.2f}")
            return False

        order_id = self._generate_order_id()
        self.balance -= cost
        self.positions[symbol.upper()] = self.positions.get(symbol.upper(), 0) + quantity
        self._record_trade(order_id, "BUY", symbol, quantity, price, cost)
        console.print(f"[green]BUY order {order_id} for {quantity} of {symbol.upper()} at ${price:.2f} filled. Remaining balance: ${self.balance:.2f}[/green]")
        return True

    def sell(self, symbol, quantity, price):
        """Simulate a sell order."""
        if self.positions.get(symbol.upper(), 0) < quantity:
            console.print(f"[bold red]Error:[/bold red] Insufficient {symbol.upper()} to sell. Available: {self.positions.get(symbol.upper(), 0)}, Attempted: {quantity}")
            return False

        order_id = self._generate_order_id()
        revenue = quantity * price
        self.balance += revenue
        self.positions[symbol.upper()] -= quantity
        if self.positions[symbol.upper()] == 0:
            del self.positions[symbol.upper()]
        self._record_trade(order_id, "SELL", symbol, quantity, price, revenue)
        console.print(f"[green]SELL order {order_id} for {quantity} of {symbol.upper()} at ${price:.2f} filled. Remaining balance: ${self.balance:.2f}[/green]")
        return True

    def view_balance(self):
        """Display current cash balance."""
        console.print(f"[bold blue]Current Cash Balance:[/bold blue] [green]${self.balance:.2f}[/green]")

    def view_positions(self):
        """Display current open positions."""
        if not self.positions:
            console.print("[yellow]No open positions.[/yellow]")
            return

        table = Table(title="[bold blue]Open Positions[/bold blue]")
        table.add_column("Symbol", style="cyan")
        table.add_column("Quantity", style="magenta", justify="right")

        for symbol, quantity in self.positions.items():
            table.add_row(symbol, str(quantity))
        console.print(table)

    def view_trade_history(self):
        """Display trade history."""
        if self.trade_history.empty:
            console.print("[yellow]No trade history.[/yellow]")
            return

        table = Table(title="[bold blue]Trade History[/bold blue]")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Order ID", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Symbol", style="green")
        table.add_column("Quantity", justify="right")
        table.add_column("Price", justify="right")
        table.add_column("Value", justify="right")
        table.add_column("Status", style="blue")

        for index, row in self.trade_history.iterrows():
            table.add_row(
                str(row["Timestamp"]).split(".")[0], # Remove microseconds
                row["OrderID"],
                row["Type"],
                row["Symbol"],
                str(row["Quantity"]),
                f"{row['Price']:.2f}",
                f"{row['Value']:.2f}",
                row["Status"]
            )
        console.print(table)

    def connect_exchange_api(self, api_key, secret_key):
        """Placeholder for connecting to a real exchange API."""
        console.print("[yellow]Connecting to exchange API is an advanced feature and not implemented in this simulation.[/yellow]")
        console.print("[yellow]This would typically involve specific API client libraries for brokers like Alpaca or Interactive Brokers.[/yellow]")
        # In a real application, this would initialize an API client
        # self.exchange_client = SomeExchangeAPIClient(api_key, secret_key)

    def place_real_order(self, order_type, symbol, quantity, price=None):
        """Placeholder for placing a real order via exchange API."""
        console.print("[yellow]Placing real orders is an advanced feature and not implemented in this simulation.[/yellow]")
        console.print("[yellow]This would interact with the connected exchange API.[/yellow]")
        # In a real application, this would call self.exchange_client.place_order(...)




