from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
import time

console = Console()

def print_banner():
    banner = """
   ______  ________  ___________ __________
  / _  | / __  /  /  _____/  /  /  _____/
 / /_| |/ /_/ /  /  /  __   /  /  \____ \ 
/ /__| / _, _/  /  /_\_\ \ /  /____/    /
\____/ \/ |_|   \________/ \__________/ 
        ARGUS: The All-Seeing Network Eye
        """
    console.print(Panel(banner, style="bold red"))

def print_training_start(packet_count):
    console.print(f"[bold yellow]Starting Training Mode...[/bold yellow]")
    console.print(f"Capturing [cyan]{packet_count}[/cyan] baseline packets.")

def print_training_progress(current, total):
    # This could be replaced by a rich.progress bar in valid uses
    pass

def print_alert(alert_json):
    """
    Pretty print an alert using Rich
    """
    severity_color = "red" if alert_json['score'] > 0.1 else "yellow"
    
    table = Table(show_header=False, box=None)
    table.add_row("[bold]Type[/bold]", f"[{severity_color}]{alert_json['type']}[/{severity_color}]")
    table.add_row("[bold]Risk Score[/bold]", f"{alert_json['score']:.4f}")
    table.add_row("[bold]Summary[/bold]", alert_json['summary'])
    
    panel = Panel(
        table,
        title=f"[{severity_color}]ANOMALY DETECTED[/{severity_color}]",
        border_style=severity_color
    )
    console.print(panel)
