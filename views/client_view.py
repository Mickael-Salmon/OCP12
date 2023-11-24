from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from accesscontrol.database_session import with_db_session
from controllers.clients import ClientController
from models.clients import Client
import re

console = Console()

@with_db_session
def add_client_view(session):
    """
    Displays a prompt to add a new client and calls the create_client method
    on the ClientController instance to create the client.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console = Console()
    client_controller = ClientController(session)
    console.print("[bold cyan]Ajouter un nouveau client[/bold cyan]")
    full_name = Prompt.ask("Entrez le nom complet du client")
    email = Prompt.ask("Entrez l'email du client")
    # Validation du numéro de téléphone
    phone_valid = False
    while not phone_valid:
        phone = Prompt.ask("Entrez le téléphone du client")
        if not re.match(r"^(\d{3}-\d{3}-\d{4}|\d{10})$", phone.replace(" ", "")):
            console.print("[bold red]Numéro de téléphone invalide. Veuillez saisir le numéro au format 123-456-7890 ou 1234567890.[/bold red]")
        elif session.query(Client).filter(Client.phone == phone).first():
            console.print("[bold red]Ce numéro de téléphone est déjà utilisé par un autre client.[/bold red]")
        else:
            phone_valid = True

    enterprise = Prompt.ask("Entrez le nom de l'entreprise du client")
    sales_contact_id = Prompt.ask("Entrez l'ID du contact commercial")

    client_controller.create_client(full_name, email, phone, enterprise, sales_contact_id)

    console.print("[bold green]Le client a été ajouté avec succès ![/bold green]")


@with_db_session
def update_client_view(session):
    """
    Updates an existing client's information.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Modifier un client existant[/bold cyan]")
    client_id = Prompt.ask("Entrez l'ID du client à modifier")
    client_controller = ClientController(session)
    existing_client = client_controller.get_client(client_id)

    if existing_client:
        # Vérification si le client est inactif et proposition de le réactiver
        if not existing_client.is_active:
            if Prompt.ask(f"Le client {existing_client.full_name} est actuellement inactif. Voulez-vous le réactiver ? (oui/non)", choices=["oui", "non"]) == "oui":
                client_controller.update_client(client_id, is_active=True)
                console.print(f"[bold green]Le client {existing_client.full_name} a été réactivé avec succès.[/bold green]")
            else:
                console.print(f"[bold yellow]Le client {existing_client.full_name} reste inactif.[/bold yellow]")
                return

        full_name = Prompt.ask("Entrez le nouveau nom complet du client", default=existing_client.full_name)
        email = Prompt.ask("Entrez le nouvel email du client", default=existing_client.email)
        phone = existing_client.phone
        phone_valid = False

        while not phone_valid:
            phone = Prompt.ask("Entrez le nouveau téléphone du client", default=phone)
            if re.match(r"^(\d{3}-\d{3}-\d{4}|\d{10})$", phone.replace(" ", "")):
                phone_valid = True
            else:
                console.print("[bold red]Numéro de téléphone invalide. Veuillez saisir le numéro au format 123-456-7890 ou 1234567890.[/bold red]")

        enterprise = Prompt.ask("Entrez le nouveau nom de l'entreprise du client", default=existing_client.enterprise)
        sales_contact_id = Prompt.ask("Entrez le nouvel ID du contact commercial", default=str(existing_client.sales_contact_id))

        if not sales_contact_id.isdigit() or int(sales_contact_id) <= 0:
            console.print("[bold red]L'ID du contact commercial est invalide.[/bold red]")
            return

        try:
            updated_client = client_controller.update_client(client_id,
                                                            full_name=full_name,
                                                            email=email,
                                                            phone=phone,
                                                            enterprise=enterprise,
                                                            sales_contact_id=sales_contact_id)
            if updated_client:
                console.print(f"[bold green]Le client ID {client_id} a été modifié avec succès ![/bold green]")
            else:
                console.print(f"[bold red]Une erreur s'est produite lors de la mise à jour du client.[/bold red]")
        except ValueError as e:
            console.print(f"[bold red]Erreur lors de la mise à jour du client : {e}[/bold red]")
    else:
        console.print(f"[bold red]Le client ID {client_id} n'a pas été trouvé.[/bold red]")



@with_db_session
def delete_client_view(session):
    """
    Displays a prompt to delete a client and performs the deletion if authorized.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Supprimer un client[/bold cyan]")
    client_id = Prompt.ask("Entrez l'ID du client à supprimer")
    client_controller = ClientController(session)

    if client_controller.has_active_contracts(client_id):
        console.print("[bold red]Le client a des contrats actifs. Suppression non autorisée.[/bold red]")
        if Prompt.ask("Voulez-vous désactiver le client ? (oui/non)", choices=["oui", "non"]) == "oui":
            client_controller.deactivate_client(client_id)
            console.print("[bold green]Le client a été désactivé.[/bold green]")
    else:
        client_controller.delete_client(client_id)
        console.print(f"[bold green]Le client ID {client_id} a été supprimé avec succès ![/bold green]")

@with_db_session
def search_client_view(session):
    """
    Search for a client based on their name or email.

    Args:
        session: The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Rechercher un client[/bold cyan]")
    search_query = Prompt.ask("Entrez le nom ou l'email du client à rechercher")

    client_controller = ClientController(session)
    clients = client_controller.search_clients(search_query)

    if clients:
        console.print("[bold green]Clients trouvés :[/bold green]")
        for client in clients:
            console.print(f"ID: {client.id} | Nom: {client.full_name} | Email: {client.email} | Actif: {'Oui' if client.is_active else 'Non'}")
    else:
        console.print("[bold red]Aucun client correspondant à la recherche.[/bold red]")

@with_db_session
def list_clients_view(session):
    """
    Display a table of clients with their ID, name, email, phone, and enterprise.

    Args:
        session: The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Liste des clients[/bold cyan]")
    client_controller = ClientController(session)
    clients = client_controller.list_clients()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")
    table.add_column("Entreprise")

    for client in clients:
        table.add_row(
            str(client.id),
            client.full_name,
            client.email,
            client.phone,
            client.enterprise
        )

    console.print(table)