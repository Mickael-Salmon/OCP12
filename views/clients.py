from rich.console import Console
from rich.table import Table

def show_clients(client_controller):
    clients = client_controller.list_clients()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")

    for client in clients:
        table.add_row(
            str(client.id),
            client.name,
            client.email,
            client.phone
        )

    console = Console()
    console.print(table)
