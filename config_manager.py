import json
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

CONFIG_FILE = os.path.join(os.path.expanduser("~/.quant_app_config.json"))

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class ConfigManager:
    def __init__(self):
        self.config = load_config()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        save_config(self.config)
        console.print(f"[green]Configuration \'{key}\' set to \'{value}\'.[/green]")

    def delete(self, key):
        if key in self.config:
            del self.config[key]
            save_config(self.config)
            console.print(f"[green]Configuration \'{key}\' deleted.[/green]")
        else:
            console.print(f"[yellow]Configuration \'{key}\' not found.[/yellow]")

    def show(self):
        if self.config:
            console.print(Panel(json.dumps(self.config, indent=4), title="[bold blue]Current Configuration[/bold blue]"))
        else:
            console.print("[yellow]No configuration settings found.[/yellow]")

    def set_alias(self, alias, command):
        aliases = self.config.get("aliases", {})
        aliases[alias] = command
        self.config["aliases"] = aliases
        save_config(self.config)
        console.print(f"[green]Alias \'{alias}\' set to \'{command}\'.[/green]")

    def get_alias(self, alias):
        aliases = self.config.get("aliases", {})
        return aliases.get(alias)

    def delete_alias(self, alias):
        aliases = self.config.get("aliases", {})
        if alias in aliases:
            del aliases[alias]
            self.config["aliases"] = aliases
            save_config(self.config)
            console.print(f"[green]Alias \'{alias}\' deleted.[/green]")
        else:
            console.print(f"[yellow]Alias \'{alias}\' not found.[/yellow]")

    def list_aliases(self):
        aliases = self.config.get("aliases", {})
        if aliases:
            table = Table(title="[bold blue]Configured Aliases[/bold blue]")
            table.add_column("Alias", style="cyan")
            table.add_column("Command", style="magenta")
            for alias, command in aliases.items():
                table.add_row(alias, command)
            console.print(table)
        else:
            console.print("[yellow]No aliases configured.[/yellow]")

    def set_theme(self, theme_name):
        # This is a placeholder for theme implementation.
        # In a real application, you would load different rich.theme.Theme objects
        # or adjust console styles based on the theme_name.
        self.config["theme"] = theme_name
        save_config(self.config)
        console.print(f"[green]Theme set to \'{theme_name}\'. (Theme application is conceptual)[/green]")

    def get_theme(self):
        return self.config.get("theme", "default")



