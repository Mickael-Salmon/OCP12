import json
import datetime
from sqlalchemy.orm import Session
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from managers import manager
from managers.manager import drop_tables, create_tables
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event

# Initialize the Rich console
console = Console()

# Drop all tables
drop_tables()
console.print(Panel("All TABLES have been [bold red]DELETED[/bold red]"), justify="left")

# Recreate tables
create_tables()
console.print(Panel("All TABLES have been [bold green]RECREATED[/bold green]"), justify="left")

def create_employees():
    console.print("[bold cyan]Creating employees...[/bold cyan]")
    data_path = Path("database", "employees_data.json")
    with open(data_path, "rb") as reader:
        employees_data = json.loads(reader.read())
    session = Session(manager.engine)
    employees = []
    for data in employees_data:
        new_employee = Employee(
            full_name=data["full_name"],
            email=data["email"],
            department=data["department"],
        )
        new_employee.set_password(password="password")
        employees.append(new_employee)
    session.add_all(employees)
    session.commit()
    console.print("[bold green]Employees have been created successfully ![/bold green]")

def create_clients():
    console.print("[bold cyan]Creating clients...[/bold cyan]")
    data_path = Path("database", "clients_data.json")
    with open(data_path, "rb") as reader:
        clients_data = json.loads(reader.read())
    session = Session(manager.engine)
    clients = [
        Client(
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            enterprise=data["enterprise"],
            sales_contact_id=data["sales_contact_id"],
        )
        for data in clients_data
    ]
    session.add_all(clients)
    session.commit()
    console.print("[bold green]All clients have been created successfully ![/bold green]")

def create_contracts():
    console.print("[bold cyan]Creating contracts...[/bold cyan]")
    data_path = Path("database", "contracts_data.json")
    with open(data_path, "rb") as reader:
        contracts_data = json.loads(reader.read())
    session = Session(manager.engine)
    contracts = [
        Contract(
            total_amount=data["total_amount"],
            to_be_paid=data["to_be_paid"],
            is_signed=data["is_signed"],
            client_id=data["client_id"],
            account_contact_id=data["account_contact_id"],
        )
        for data in contracts_data
    ]
    session.add_all(contracts)
    session.commit()
    console.print("[bold green]All contracts have been created successfully[/bold green]")

def create_events():
    console.print("[bold cyan]Creating events...[/bold cyan]")
    data_path = Path("database", "events_data.json")
    with open(data_path, "rb") as reader:
        events_data = json.loads(reader.read())
    session = Session(manager.engine)
    events = [
        Event(
            start_date=datetime.datetime.fromisoformat(data["start_date"]),
            end_date=datetime.datetime.fromisoformat(data["end_date"]),
            location=data["location"],
            attendees_count=data["attendees_count"],
            notes=data["notes"],
            support_contact_id=data.get("support_contact_id", None),
        )
        for data in events_data
    ]
    session.add_all(events)
    session.commit()
    console.print("[bold green]All events have been created successfully ![/bold green]")

if __name__ == "__main__":
    create_employees()
    create_clients()
    create_contracts()
    create_events()
