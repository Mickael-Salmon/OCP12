"""
This script is responsible for populating the database tables with initial data.
It reads JSON files containing the data for employees, clients, contracts, and events
and then adds these records to the respective tables in the database.
This is usually run once when setting up the application to ensure that the database is in a usable state.
"""
import json
import datetime
from sqlalchemy.orm import Session
from pathlib import Path

from managers import manager
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event


def create_employees():
    """
    Populate the Employee table in the database from data found in `database/employees_data.json`.
    """
    print("Creating employees...")
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


def create_clients():
    """
    Populate the Client table in the database from data found in `database/clients_data.json`.
    """
    print("Creating clients...")
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


def create_contracts():
    """
    Populate the Contract table in the database from data found in `database/contracts_data.json`.
    """
    print("Creating contracts...")
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


def create_events():
    """
    Populate the Event table in the database from data found in `database/events_data.json`.
    """
    print("Creating events...")
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
            support_contact_id=data["support_contact_id"],
        )
        for data in events_data
    ]
    session.add_all(events)
    session.commit()


if __name__ == "__main__":
    """
    Reset the database tables and populate them with initial data.
    """
    manager.drop_tables()
    manager.create_tables()
    create_employees()
    create_clients()
    create_contracts()
    create_events()
