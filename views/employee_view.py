from rich.prompt import Prompt
from rich.console import Console
from accesscontrol.database_session import with_db_session
from models.employees import Department
from controllers.employees import EmployeeController

console = Console()

@with_db_session
def list_employees_view(session):
    console.print("[bold cyan]Liste des employés[/bold cyan]")
    employee_controller = EmployeeController(session)
    employee_controller.list_employees()

@with_db_session
def add_employee_view(session):
    console.print("[bold cyan]Ajouter un nouvel employé[/bold cyan]")
    full_name = Prompt.ask("Entrez le nom complet de l'employé")
    email = Prompt.ask("Entrez l'email de l'employé")
    department_choices = [d.value for d in Department]
    department = Prompt.ask("Entrez le département de l'employé", choices=department_choices)
    password = Prompt.ask("Entrez le mot de passe de l'employé", password=True)

    # Convertir le département en majuscules pour correspondre à l'énumération
    department = department.upper()

    employee_controller = EmployeeController(session)
    employee_controller.create_employee(full_name, email, department, password)

    console.print("[bold green]L'employé a été ajouté avec succès ![/bold green]")


@with_db_session
def update_employee_view(session):
    console.print("[bold cyan]Modifier un employé existant[/bold cyan]")
    employee_id = Prompt.ask("Entrez l'ID de l'employé à modifier")
    employee_controller = EmployeeController(session)
    existing_employee = employee_controller.get_employee(employee_id)

    if existing_employee:
        full_name = Prompt.ask("Entrez le nouveau nom complet de l'employé", default=existing_employee.full_name)
        email = Prompt.ask("Entrez le nouvel email de l'employé", default=existing_employee.email)
        department_choices = [d.value for d in Department]
        department = Prompt.ask("Entrez le nouveau département de l'employé", choices=department_choices, default=existing_employee.department.value.upper())

        # Assurez-vous que la valeur saisie est convertie en majuscules pour correspondre à l'énumération
        department = department.upper() if department.lower() in [d.value.lower() for d in Department] else existing_employee.department.value

        # Appel de la méthode update_employee du EmployeeController avec les nouvelles valeurs
        updated_employee = employee_controller.update_employee(employee_id,
                                                            full_name=full_name,
                                                            email=email,
                                                            department=department)

        if updated_employee:
            console.print(f"[bold green]L'employé ID {employee_id} a été modifié avec succès ![/bold green]")
        else:
            console.print(f"[bold red]Une erreur s'est produite lors de la mise à jour de l'employé.[/bold red]")
    else:
        console.print(f"[bold red]L'employé ID {employee_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def delete_employee_view(session):
    console.print("[bold cyan]Supprimer un employé[/bold cyan]")
    employee_id = Prompt.ask("Entrez l'ID de l'employé à supprimer")
    employee_controller = EmployeeController(session)

    existing_employee = employee_controller.get_employee(employee_id)
    if existing_employee:
        if Prompt.ask(f"Êtes-vous sûr de vouloir supprimer l'employé {existing_employee.full_name}? (oui/non)", choices=["oui", "non"]) == "oui":
            employee_controller.delete_employee(employee_id)
            console.print(f"[bold green]L'employé ID {employee_id} a été supprimé avec succès ![/bold green]")
        else:
            console.print("[bold yellow]Suppression annulée.[/bold yellow]")
    else:
        console.print(f"[bold red]L'employé ID {employee_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def search_employee_view(session):
    console.print("[bold cyan]Rechercher un employé[/bold cyan]")
    search_query = Prompt.ask("Entrez l'ID de l'employé ou le nom à rechercher")

    employee_controller = EmployeeController(session)
    employees = employee_controller.search_employees(search_query)

    if employees:
        console.print("[bold green]Employés trouvés :[/bold green]")
        for employee in employees:
            console.print(f"ID: {employee.id} | Nom: {employee.full_name} | Email: {employee.email} | Département: {employee.department.value}")
    else:
        console.print("[bold red]Aucun employé correspondant à la recherche.[/bold red]")
