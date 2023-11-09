# Importations
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from accesscontrol.sec_sessions import authenticated_action, admin_required
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

# Initialisation de la console
console = Console()

# Navigation Menu
def show_menu(title, options, actions):
    console.print(f"[bold cyan]{title}[/bold cyan]", justify="center")
    for i, option in enumerate(options, 1):
        console.print(f"[{i}] {option}")
    options.append("Retour au menu principal")
    choice = Prompt.ask("Choisis une option", choices=[str(i) for i in range(1, len(options) + 1)], default="1")
    if choice == str(len(options)):
        return
    else:
        actions[int(choice) - 1]()

# Menu Principal
def show_main_menu():
    console.print("[bold magenta]Epic Events CRM[/bold magenta]", justify="center")
    options = [
        "Gestion des clients",
        "Gestion des contrats",
        "Gestion des événements",
        "Administration des employés",
        "Rapports et analyses",
        "Se connecter",
        "Se déconnecter",
        "Quitter"]
    actions = [
        show_clients_menu,
        show_contracts_menu,
        show_events_menu,
        show_administration_menu,
        show_reports_menu,
        login_view,
        logout_view,
        quit_app
        ]
    show_menu("Menu Principal", options, actions)

# Menu Clients
@authenticated_action
def show_clients_menu():
    title = "Gestion des clients"
    options = ["Ajouter un client", "Modifier un client", "Supprimer un client", "Rechercher un client"]
    actions = [add_client_view, update_client_view, delete_client_view, search_client_view]
    show_menu(title, options, actions)

# Menu Contrats
@authenticated_action
def show_contracts_menu():
    title = "Gestion des contrats"
    options = ["Voir tous les contrats", "Ajouter un contrat", "Modifier un contrat",
               "Supprimer un contrat", "Rechercher un contrat"]
    actions = [list_contracts_view, add_contract_view, update_contract_view, delete_contract_view, search_contract_view]
    show_menu(title, options, actions)

# Menu Événements
@authenticated_action
def show_events_menu():
    title = "Gestion des événements"
    options = ["Ajouter un événement", "Modifier un événement", "Supprimer un événement", "Rechercher un événement"]
    actions = [add_event_view, update_event_view, delete_event_view, search_event_view]
    show_menu(title, options, actions)

# Menu Administration
@admin_required
def show_administration_menu():
    title = "Administration des employés"
    options = ["Ajouter un employé", "Modifier un employé", "Supprimer un employé",
               "Rechercher un employé", "Liste des employés"]
    actions = [add_employee_view, update_employee_view, delete_employee_view, search_employee_view, list_employees_view]
    show_menu(title, options, actions)

# Menu Rapports et Analyses
@authenticated_action
def show_reports_menu():
    title = "Rapports et analyses"
    options = ["Générer un rapport de clients", "Générer un rapport de contrats",
               "Générer un rapport d'événements", "Analyse des données"]
    actions = []  # TODO: Ajouter les fonctions d'action correspondantes
    show_menu(title, options, actions)

# Quitter l'application
def quit_app():
    console.print("[bold green]À bientôt ![/bold green]")
    exit(0)

# Point d'entrée principal
if __name__ == "__main__":
    while True:
        show_main_menu()