from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from accesscontrol.sec_sessions import authenticated_action, admin_required, permission_required
from models.employees import Department
from views.login_view import login_view
from views.logout_view import logout_view
from utils.token_storage import load_token, delete_token
from views.client_view import (
    add_client_view,
    update_client_view,
    delete_client_view,
    search_client_view
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
console = Console()

# def admin_required(action):
#     """
#     Decorateur qui vérifie que l'utilisateur connecté est un administrateur avant de permettre l'exécution d'une action.
#     """
#     def wrapper(*args, **kwargs):
#         token = load_token()
#         current_user = load_current_user(token)
#         if not current_user or current_user.department != 'ADMIN':  # 'ADMIN' est la valeur pour les admins
#             console.print("[bold red]Accès refusé : Vous devez être connecté en tant qu'administrateur pour accéder à cette fonctionnalité.[/bold red]")
#             return
#         return action(*args, **kwargs)
#     return wrapper


# def authenticated_action_wrapper(action):
#     """
#     Decorateur qui vérifie la présence d'un token avant de permettre l'exécution d'une action nécessitant une authentification.
#     """
#     def wrapper(*args, **kwargs):
#         if not load_token():
#             console.print("[bold red]Vous n'êtes pas connecté. Veuillez vous connecter.[/bold red]")
#             login_view()
#             if not load_token():
#                 console.print("[bold red]Échec de la connexion. Action annulée.[/bold red]")
#                 return
#         return action(*args, **kwargs)
#     return wrapper

@authenticated_action
def show_clients_menu():
    console.print("[bold cyan]Gestion des clients[/bold cyan]", justify="center")
    console.print("[1] Ajouter un client")
    console.print("[2] Modifier un client")
    console.print("[3] Supprimer un client")
    console.print("[4] Rechercher un client")
    console.print("[5] Retour au menu principal")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5"], default="1")

    if choice == "1":
        add_client_view()
    elif choice == "2":
        update_client_view()
        pass
    elif choice == "3":
        delete_client_view()
        pass
    elif choice == "4":
        search_client_view()
        pass
    elif choice == "5":
        return

@authenticated_action
def show_contracts_menu():
    console.print("[bold cyan]Gestion des contrats[/bold cyan]", justify="center")
    console.print("[1] Voir tous les contrats")
    console.print("[2] Ajouter un contrat")
    console.print("[3] Modifier un contrat")
    console.print("[4] Supprimer un contrat")
    console.print("[5] Rechercher un contrat")
    console.print("[6] Retour au menu principal")

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
        # Retour au menu principal
        return
    else:
        console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

@authenticated_action
def show_events_menu():
    console.print("[bold cyan]Gestion des événements[/bold cyan]", justify="center")
    console.print("[1] Ajouter un événement")
    console.print("[2] Modifier un événement")
    console.print("[3] Supprimer un événement")
    console.print("[4] Rechercher un événement")
    console.print("[5] Retour au menu principal")
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
        console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")


@admin_required
def show_administration_menu():
    console.print("[bold cyan]Administration des employés[/bold cyan]", justify="center")
    console.print("[1] Ajouter un employé")
    console.print("[2] Modifier un employé")
    console.print("[3] Supprimer un employé")
    console.print("[4] Rechercher un employé")
    console.print("[5] Liste des employés")
    console.print("[6] Retour au menu principal")

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
        # Retour au menu principal
        return
    else:
        console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")

@authenticated_action
def show_reports_menu():
    console.print("[bold cyan]Rapports et analyses[/bold cyan]", justify="center")
    console.print("[1] Générer un rapport de clients")
    console.print("[2] Générer un rapport de contrats")
    console.print("[3] Générer un rapport d'événements")
    console.print("[4] Analyse des données")
    console.print("[5] Retour au menu principal")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5"], default="1")
    # TODO: Implémenter les actions pour les rapports et analyses
    if choice == "5":
        return

def show_main_menu():
    console.print("[bold magenta]Epic Events CRM[/bold magenta]", justify="center")
    console.print("[1] Gestion des clients")
    console.print("[2] Gestion des contrats")
    console.print("[3] Gestion des événements")
    console.print("[4] Administration des utilisateurs")
    console.print("[5] Rapports et analyses")
    console.print("[6] Se connecter")
    console.print("[7] Se déconnecter")
    console.print("[8] Quitter")
    choice = Prompt.ask("Choisis une option", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")
    return choice

def main():
    while True:
        choice = show_main_menu()
        if choice == "1":
            show_clients_menu()
        elif choice == "2":
            show_contracts_menu()
        elif choice == "3":
            show_events_menu()
        elif choice == "4":
            show_administration_menu()
        elif choice == "5":
            show_reports_menu()
        elif choice == "6":
            if not load_token():
                login_view()
        elif choice == "7":
            if load_token():
                logout_view()
                delete_token()
                console.print("[bold green]Vous avez été déconnecté avec succès.[/bold green]")
        elif choice == "8":
            console.print("[bold green]À bientôt ![/bold green]")
            break

if __name__ == "__main__":
    main()
