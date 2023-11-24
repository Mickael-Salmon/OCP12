from models.employees import Employee
from rich.console import Console
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
# from werkzeug.security import generate_password_hash
import bcrypt
class EmployeeController:
    """
    Controller class for managing employees.
    """

    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_employees(self):
        """
        Retrieves a list of all employees from the database.

        Returns:
            List[Employee]: A list of Employee objects.
        """
        employees = self.session.query(Employee).all()
        self.console.print("[bold green]Liste des employés :[/bold green]")
        for employee in employees:
            self.console.print(f"ID: {employee.id} | Nom: {employee.full_name} | Email: {employee.email} | Département: {employee.department}")
        return employees

    def get_employee(self, employee_id):
        """
        Retrieves an employee by their ID.

        Args:
            employee_id (int): The ID of the employee.

        Returns:
            Employee: The Employee object if found, None otherwise.
        """
        employee = self.session.query(Employee).get(employee_id)
        if employee:
            self.console.print(f"[bold green]Employé trouvé :[/bold green] ID {employee.id} - {employee.full_name}")
        else:
            self.console.print("[bold red]Employé non trouvé.[/bold red]")
        return employee

    def create_employee(self, full_name, email, department, password):
        """
        Creates a new employee.

        Args:
            full_name (str): The full name of the employee.
            email (str): The email address of the employee.
            department (str): The department of the employee.
            password (str): The password for the employee.

        Returns:
            Employee: The newly created Employee object.

        Raises:
            SQLAlchemyError: If an error occurs during the creation process.
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
            password_hash=hashed_password.decode('utf-8')  # Stocke le hash sous forme de string
        )
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
        """
        Updates an employee with the given attributes.

        Args:
            employee_id (int): The ID of the employee.
            **kwargs: The attributes to update.

        Returns:
            Employee: The updated Employee object.

        Raises:
            SQLAlchemyError: If an error occurs during the update process.
        """
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
        """
        Deletes an employee by their ID.

        Args:
            employee_id (int): The ID of the employee.

        Raises:
            SQLAlchemyError: If an error occurs during the deletion process.
        """
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
        """
        Searches for employees based on a search query.

        Args:
            search_query (str): The search query.

        Returns:
            List[Employee]: A list of Employee objects matching the search query.
        """
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


