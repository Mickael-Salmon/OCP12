from models.employees import Employee
from rich.console import Console
from sqlalchemy import or_

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

    def create_employee(self, full_name, email, department, password="password"):
        try:
            new_employee = Employee(
                full_name=full_name,
                email=email,
                department=department
            )
            new_employee.set_password(password)  # Définir le mot de passe
            self.session.add(new_employee)
            self.session.commit()
            self.console.print("[bold green]Employé créé avec succès ![/bold green]")
            return new_employee
        except Exception as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création de l'employé : {e}[/bold red]")
            raise


    def update_employee(self, employee_id, **kwargs):
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            for attr, value in kwargs.items():
                setattr(employee, attr, value)
            self.session.commit()
            self.console.print(f"[bold green]Employé mis à jour : ID {employee.id}[/bold green]")
            return employee
        else:
            self.console.print("[bold red]Employé non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_employee(self, employee_id):
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            self.session.delete(employee)
            self.session.commit()
            self.console.print(f"[bold green]Employé supprimé : ID {employee.id}[/bold green]")
        else:
            self.console.print("[bold red]Employé non trouvé pour suppression.[/bold red]")

    def search_employees(self, search_query):
        if search_query.isdigit():  # Si la recherche est un nombre, on cherche par ID.
            employee_id = int(search_query)
            return self.session.query(Employee).filter(Employee.id == employee_id).all()
        else:  # Sinon, on cherche par nom en utilisant ILIKE.
            search = f"%{search_query}%"
            return self.session.query(Employee).filter(
                or_(Employee.full_name.ilike(search), Employee.email.ilike(search))
            ).all()
