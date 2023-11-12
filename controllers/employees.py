from models.employees import Employee
from rich.console import Console
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

class EmployeeController:
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_employees(self):
        employees = self.session.query(Employee).all()
        self.console.print("[bold green]Liste des employés :[/bold green]")
        for employee in employees:
            self.console.print(f"ID: {employee.id} | Nom: {employee.full_name} | Email: {employee.email} | Département: {employee.department}")
        return employees

    def get_employee(self, employee_id):
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            self.console.print(f"[bold green]Employé trouvé :[/bold green] ID {employee.id} - {employee.full_name}")
        else:
            self.console.print("[bold red]Employé non trouvé.[/bold red]")
        return employee

    def create_employee(self, full_name, email, department, password):
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department
        )
        new_employee.password_hash = generate_password_hash(password)
        try:
            self.session.add(new_employee)
            self.session.commit()
            self.console.print("[bold green]Employé créé avec succès ![/bold green]")
            return new_employee
        except SQLAlchemyError as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création de l'employé : {e}[/bold red]")
            raise

    def update_employee(self, employee_id, **kwargs):
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            for attr, value in kwargs.items():
                setattr(employee, attr, value)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Employé mis à jour : ID {employee.id}[/bold green]")
                return employee
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la mise à jour de l'employé : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Employé non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_employee(self, employee_id):
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            self.session.delete(employee)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Employé supprimé : ID {employee.id}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la suppression de l'employé : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Employé non trouvé pour suppression.[/bold red]")

    def search_employees(self, search_query):
        try:
            search_query_int = int(search_query)
            employees = self.session.query(Employee).filter(
                or_(
                    Employee.full_name.ilike(f"%{search_query}%"),
                    Employee.id == search_query_int
                )
            ).all()
        except ValueError:  # Si la conversion en int échoue, ce n'est pas un ID
            employees = self.session.query(Employee).filter(
                Employee.full_name.ilike(f"%{search_query}%")
            ).all()
        return employees


