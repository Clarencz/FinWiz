import pandas as pd
from rich.console import Console
from rich.table import Table
from fpdf import FPDF
import os

console = Console()

class Reporting:
    def __init__(self):
        pass

    def export_dataframe_to_csv(self, df, filename="output.csv"):
        """Export a pandas DataFrame to a CSV file."""
        try:
            df.to_csv(filename, index=False)
            console.print(f"[green]DataFrame successfully exported to {filename}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error exporting to CSV:[/bold red] {e}")

    def export_dataframe_to_excel(self, df, filename="output.xlsx"):
        """Export a pandas DataFrame to an Excel file."""
        try:
            df.to_excel(filename, index=False)
            console.print(f"[green]DataFrame successfully exported to {filename}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error exporting to Excel:[/bold red] {e}")

    def generate_pdf_report(self, title, content_dict, filename="report.pdf"):
        """Generate a simple PDF report from a dictionary of content."""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, title, 0, 1, "C")
            pdf.ln(10)

            pdf.set_font("Arial", "", 12)
            for section_title, section_content in content_dict.items():
                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, section_title, 0, 1, "L")
                pdf.set_font("Arial", "", 12)
                if isinstance(section_content, pd.DataFrame):
                    # Convert DataFrame to string for PDF
                    pdf.multi_cell(0, 5, section_content.to_string())
                else:
                    pdf.multi_cell(0, 5, str(section_content))
                pdf.ln(5)

            pdf.output(filename)
            console.print(f"[green]PDF report successfully generated to {filename}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error generating PDF report:[/bold red] {e}")

    def send_email_alert(self, recipient, subject, body):
        """Simulate sending an email alert."""
        console.print("[yellow]Email alert functionality is a placeholder. Requires SMTP server configuration.[/yellow]")
        console.print(f"[green]Simulating email to {recipient} with subject \'{subject}\' and body:\n{body}[/green]")

    def send_terminal_notification(self, message, style="green"):
        """Send a colored terminal notification."""
        console.print(f"[{style}]{message}[/{style}]")


