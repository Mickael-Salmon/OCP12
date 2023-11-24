from rich.console import Console
from rich.table import Table
from accesscontrol.database_session import with_db_session
from controllers.reports import ReportController
from models.contracts import Contract

console = Console()

@with_db_session
def events_per_client_view(session):
    """
    Displays a table showing the number of events per client.

    Args:
        session: The session object for database connection.

    Returns:
        None
    """
    report_controller = ReportController(session)
    event_counts = report_controller.get_event_count_by_client()

    table = Table(title="Nombre d'événements par client", show_header=True, header_style="bold magenta")
    table.add_column("Client", style="bold")
    table.add_column("Nombre d'événements", justify="right")

    for client_name, event_count in event_counts:
        table.add_row(client_name, str(event_count))

    console.print(table)

@with_db_session
def contracts_per_sales_view(session):
    """
    Displays a table showing the number of contracts per salesperson.

    Args:
        session: The session object for database connection.

    Returns:
        None
    """
    report_controller = ReportController(session)
    contract_counts = report_controller.get_contract_count_by_sales()

    table = Table(title="Nombre de contrats par commercial", show_header=True, header_style="bold magenta")
    table.add_column("Commercial", style="bold")
    table.add_column("Nombre de contrats", justify="right")

    for sales_name, contract_count in contract_counts:
        table.add_row(sales_name, str(contract_count))

    console.print(table)

@with_db_session
def events_per_support_view(session):
    """
    Display a table showing the number of events per support.

    Args:
        session: The session object used for database connection.

    Returns:
        None
    """
    report_controller = ReportController(session)
    event_counts = report_controller.get_event_count_by_support()

    table = Table(title="Nombre d'événements par support", show_header=True, header_style="bold magenta")
    table.add_column("Support", style="bold")
    table.add_column("Nombre d'événements", justify="right")

    for support_name, event_count in event_counts:
        table.add_row(support_name, str(event_count))

    console.print(table)

@with_db_session
def total_revenue_view(session):
    """
    Display the total revenue.

    Args:
        session: The session object.

    Returns:
        None
    """
    console.print("[bold cyan]Chiffre d'affaires total[/bold cyan]")
    report_controller = ReportController(session)
    total_revenue = report_controller.get_total_revenue()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Chiffre d'affaires total", justify="right")

    table.add_row(f"{total_revenue:.2f} €")

    console.print(table)

@with_db_session
def contracts_signed_status_view(session):
    """
    Display a report of signed and unsigned contracts.

    Args:
        session (Session): The database session.

    Returns:
        None
    """
    console.print("[bold cyan]Rapport des contrats signés et non signés[/bold cyan]")
    signed_contracts = session.query(Contract).filter_by(is_signed=True).count()
    unsigned_contracts = session.query(Contract).filter_by(is_signed=False).count()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("État du contrat", style="dim")
    table.add_column("Nombre")

    table.add_row("Signés", str(signed_contracts))
    table.add_row("Non Signés", str(unsigned_contracts))

    console.print(table)
