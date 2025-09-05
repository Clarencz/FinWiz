from cryptography.fernet import Fernet
import os
from rich.console import Console

console = Console()

class SecurityManager:
    def __init__(self, key_file="encryption.key"):
        self.key_file = key_file
        self.key = self._load_or_generate_key()
        self.fernet = Fernet(self.key)

    def _load_or_generate_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
            console.print("[green]Loaded encryption key from file.[/green]")
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            console.print("[green]Generated new encryption key and saved to file.[/green]")
        return key

    def encrypt_data(self, data):
        """Encrypts a string of data."""
        encoded_data = data.encode()
        encrypted_data = self.fernet.encrypt(encoded_data)
        console.print("[green]Data encrypted.[/green]")
        return encrypted_data.decode() # Return as string for easier storage

    def decrypt_data(self, encrypted_data):
        """Decrypts an encrypted string of data."""
        try:
            decrypted_data = self.fernet.decrypt(encrypted_data.encode())
            console.print("[green]Data decrypted.[/green]")
            return decrypted_data.decode()
        except Exception as e:
            console.print(f"[bold red]Error decrypting data:[/bold red] {e}")
            return None

    def encrypt_file(self, input_filepath, output_filepath):
        """Encrypts the content of a file."""
        try:
            with open(input_filepath, "rb") as f:
                file_data = f.read()
            encrypted_file_data = self.fernet.encrypt(file_data)
            with open(output_filepath, "wb") as f:
                f.write(encrypted_file_data)
            console.print(f"[green]File \'{input_filepath}\' encrypted to \'{output_filepath}\'[/green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error encrypting file:[/bold red] {e}")
            return False

    def decrypt_file(self, input_filepath, output_filepath):
        """Decrypts the content of an encrypted file."""
        try:
            with open(input_filepath, "rb") as f:
                encrypted_file_data = f.read()
            decrypted_file_data = self.fernet.decrypt(encrypted_file_data)
            with open(output_filepath, "wb") as f:
                f.write(decrypted_file_data)
            console.print(f"[green]File \'{input_filepath}\' decrypted to \'{output_filepath}\'[/green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error decrypting file:[/bold red] {e}")
            return False

    def setup_authentication(self, username, password):
        """Placeholder for setting up user authentication."""
        console.print("[yellow]User authentication is a conceptual feature. Implementation would involve hashing passwords and managing user sessions.[/yellow]")
        # In a real application, you would hash the password and store it securely
        # For example: hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # Store username and hashed_password
        console.print(f"[green]Authentication setup for user: {username}[/green]")

    def verify_authentication(self, username, password):
        """Placeholder for verifying user authentication."""
        console.print("[yellow]User authentication verification is a conceptual feature.[/yellow]")
        # In a real application, you would retrieve the hashed password for the username
        # and compare it with the provided password
        # For example: bcrypt.checkpw(password.encode(), stored_hashed_password)
        if username == "test" and password == "password": # Simple placeholder check
            console.print("[green]Authentication successful.[/green]")
            return True
        else:
            console.print("[bold red]Authentication failed.[/bold red]")
            return False

    def enable_sandbox_mode(self):
        """Placeholder for enabling sandbox mode."""
        console.print("[yellow]Sandbox mode is a conceptual feature. Implementation would involve restricting file system access and network operations.[/yellow]")
        console.print("[green]Sandbox mode enabled.[/green]")

    def disable_sandbox_mode(self):
        """Placeholder for disabling sandbox mode."""
        console.print("[yellow]Sandbox mode is a conceptual feature.[/yellow]")
        console.print("[green]Sandbox mode disabled.[/green]")


