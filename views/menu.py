from rich.console import Console
from rich.prompt import Prompt
from rich import text
from rich.panel import Panel
from rich import box
from rich.table import Table
from accesscontrol.sec_sessions import authenticated_action, admin_required, permission_required
from accesscontrol.auth_decorators import authenticated, admin_required
from models.employees import Department
from views.login_view import login_view
from views.logout_view import logout_view
from views.client_view import (
    add_client_view,
    update_client_view,
    delete_client_view,
    search_client_view,
    list_clients_view
)
from views.contract_view import (
    add_contract_view,
    update_contract_view,
    delete_contract_view,
    search_contract_view,
    list_contracts_view
)
from views.event_view import (
    list_events_view,
    add_event_view,
    update_event_view,
    delete_event_view,
    search_event_view
)
from views.employee_view import (
    add_employee_view,
    update_employee_view,
    delete_employee_view,
    search_employee_view,
    list_employees_view
)
from views.report_view import (
    events_per_client_view,
    contracts_per_sales_view,
    events_per_support_view,
    total_revenue_view,
    contracts_signed_status_view
)
console = Console()

@authenticated
def show_clients_menu(*args, **kwargs):
    """
    Displays the clients menu and handles user input.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments. Expected keyword arguments are:
            - user: The user object.
            - user_id: The user ID.
            - token: The authentication token.

    Returns:
        None
    """
    user = kwargs['user']
    user_id = kwargs.get('user_id')
    token = kwargs.get('token')

    console.print(Panel("[bold cyan]Gestion des clients[/bold cyan]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Ajouter un client")
    table.add_row("[2] Modifier un client")
    table.add_row("[3] Supprimer un client")
    table.add_row("[4] Rechercher un client")
    table.add_row("[5] Liste des clients")
    table.add_row("[6] Retour au menu principal")

    console.print(table, justify="center")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5", "6"], default="1")

    if choice == "1":
        add_client_view()
    elif choice == "2":
        update_client_view()
    elif choice == "3":
        delete_client_view()
    elif choice == "4":
        search_client_view()
    elif choice == "5":
        list_clients_view()
    elif choice == "6":
        return  # Retour au menu principal
    else:
        console.print(Panel("[bold red]Choix invalide, veuillez réessayer.[/bold red]", expand=False))


@authenticated
def show_contracts_menu(*args, **kwargs):
    """
    Displays the contracts menu and handles user input.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments. Expected keyword arguments are:
            - user: The user object.
            - user_id: The user ID.
            - token: The authentication token.

    Returns:
        None
    """
    user = kwargs['user']
    user_id = kwargs.get('user_id')
    token = kwargs.get('token')
    console.print(Panel("[bold cyan]Gestion des contrats[/bold cyan]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Voir tous les contrats")
    table.add_row("[2] Ajouter un contrat")
    table.add_row("[3] Modifier un contrat")
    table.add_row("[4] Supprimer un contrat")
    table.add_row("[5] Rechercher un contrat")
    table.add_row("[6] Retour au menu principal")

    console.print(table, justify="center")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5", "6"], default="1")

    if choice == "1":
        list_contracts_view()
    elif choice == "2":
        add_contract_view()
    elif choice == "3":
        update_contract_view()
    elif choice == "4":
        delete_contract_view()
    elif choice == "5":
        search_contract_view()
    elif choice == "6":
        return  # Retour au menu principal
    else:
        console.print(Panel("[bold red]Choix invalide, veuillez réessayer.[/bold red]", expand=False))


@authenticated
def show_events_menu(*args, **kwargs):
    """
    Displays the events menu and handles user input.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments. Expected keyword arguments are:
            - user: The user object.
            - user_id: The user ID.
            - token: The authentication token.

    Returns:
        None
    """
    user = kwargs['user']
    user_id = kwargs.get('user_id')
    token = kwargs.get('token')
    console.print(Panel("[bold cyan]Gestion des événements[/bold cyan]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Ajouter un événement")
    table.add_row("[2] Modifier un événement")
    table.add_row("[3] Supprimer un événement")
    table.add_row("[4] Rechercher un événement")
    table.add_row("[5] Retour au menu principal")

    console.print(table, justify="center")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5"], default="1")

    if choice == "1":
        add_event_view()
    elif choice == "2":
        update_event_view()
    elif choice == "3":
        delete_event_view()
    elif choice == "4":
        search_event_view()
    elif choice == "5":
        return  # Retour au menu principal
    else:
        console.print(Panel("[bold red]Choix invalide, veuillez réessayer.[/bold red]", expand=False))



@admin_required
def show_administration_menu(*args, **kwargs):
    """
    Display the administration menu for managing employees.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments. Expected keyword arguments are:
            - user: The user object.
            - user_id: The user ID.
            - token: The authentication token.

    Returns:
        None
    """
    user = kwargs['user']
    user_id = kwargs.get('user_id')
    token = kwargs.get('token')
    console.print(Panel("[bold cyan]Administration des employés[/bold cyan]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Ajouter un employé")
    table.add_row("[2] Modifier un employé")
    table.add_row("[3] Supprimer un employé")
    table.add_row("[4] Rechercher un employé")
    table.add_row("[5] Liste des employés")
    table.add_row("[6] Retour au menu principal")

    console.print(table, justify="center")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5", "6"], default="1")

    if choice == "1":
        add_employee_view()
    elif choice == "2":
        update_employee_view()
    elif choice == "3":
        delete_employee_view()
    elif choice == "4":
        search_employee_view()
    elif choice == "5":
        list_employees_view()
    elif choice == "6":
        return  # Retour au menu principal
    else:
        console.print(Panel("[bold red]Choix invalide, veuillez réessayer.[/bold red]", expand=False))


@authenticated
def show_reports_menu(*args, **kwargs):
    """
    Display the reports menu and handle user's choice.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments. Expected keyword arguments are:
            - user: User object.
            - user_id: User ID.
            - token: User token.

    Returns:
        None
    """
    user = kwargs['user']
    user_id = kwargs.get('user_id')
    token = kwargs.get('token')

    console.print(Panel("[bold cyan]Rapports et analyses[/bold cyan]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Générer un rapport de clients")
    table.add_row("[2] Générer un rapport de contrats")
    table.add_row("[3] Générer un rapport d'événements")
    table.add_row("[4] Générer un rapport évènements par clients")
    table.add_row("[5] Générer un rapport contrats par commercial")
    table.add_row("[6] Générer un rapport évènements par support")
    table.add_row("[7] Générer un rapport sur les signatures de contrats")
    table.add_row("[8] Générer un rapport sur le chiffre d'affaires")
    table.add_row("[9] Retour au menu principal")

    console.print(table, justify="center")

    choice = Prompt.ask("Choisis une option", choices=[str(i) for i in range(1, 10)], default="1")

    if choice == "1":
        list_clients_view()
    elif choice == "2":
        list_contracts_view()
    elif choice == "3":
        list_events_view()
    elif choice == "4":
        events_per_client_view()
    elif choice == "5":
        contracts_per_sales_view()
    elif choice == "6":
        events_per_support_view()
    elif choice == "7":
        contracts_signed_status_view()
    elif choice == "8":
        total_revenue_view()
    elif choice == "9":
        return  # Retour au menu principal
    else:
        console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

def show_main_menu():
    """
    Displays the main menu of the Epic Events CRM.

    Returns:
        str: The user's choice from the menu.
    """
    console.print(Panel("[bold magenta]Epic Events CRM[/bold magenta]", expand=False), justify="center")

    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("[1] Gestion des clients")
    table.add_row("[2] Gestion des contrats")
    table.add_row("[3] Gestion des événements")
    table.add_row("[4] Administration des utilisateurs")
    table.add_row("[5] Rapports et analyses")
    table.add_row("[6] Se déconnecter")
    table.add_row("[7] Quitter")

    console.print(table, justify="center")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")

    return choice

def main():
    """
    The main function of the application.
    It displays the main menu and handles user choices.
    """
    console.print(Panel("[bold green]Bienvenue dans l'application Epic Events CRM[/bold green]", expand=False))

    # Tente de se connecter et récupère l'ID utilisateur et le token
    user_id, token = login_view()

    # Vérifie si la connexion a réussi
    if not user_id:
        console.print(Panel("[bold red]Connexion échouée. L'application va se terminer.[/bold red]", expand=False))
        return

    while True:
        choice = show_main_menu()

        if choice == "1":
            show_clients_menu(user_id=user_id, token=token)
        elif choice == "2":
            show_contracts_menu(user_id=user_id, token=token)
        elif choice == "3":
            show_events_menu(user_id=user_id, token=token)
        elif choice == "4":
            show_administration_menu(user_id=user_id, token=token)
        elif choice == "5":
            show_reports_menu(user_id=user_id, token=token)
        elif choice == "6":
            logout_view(token=token)
            console.print(Panel("[bold green]Merci et à bientôt ![/bold green]", expand=False))
            break
        elif choice == "7":
            console.print(Panel("[bold green]À bientôt ![/bold green]", expand=False))
            break


if __name__ == "__main__":
    main()
