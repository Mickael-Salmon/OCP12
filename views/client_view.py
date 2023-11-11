from rich.prompt import Prompt
from rich.console import Console
from accesscontrol.database_session import with_db_session
from controllers.clients import ClientController
from rich.console import Console
from rich.table import Table

console = Console()

@with_db_session
def add_client_view(session):
    console = Console()
    client_controller = ClientController(session)
    console.print("[bold cyan]Ajouter un nouveau client[/bold cyan]")
    full_name = Prompt.ask("Entrez le nom complet du client")
    email = Prompt.ask("Entrez l'email du client")
    phone = Prompt.ask("Entrez le téléphone du client")
    enterprise = Prompt.ask("Entrez le nom de l'entreprise du client")
    sales_contact_id = Prompt.ask("Entrez l'ID du contact commercial")

    # Appel de la méthode create_client sur l'instance de ClientController
    client_controller.create_client(full_name, email, phone, enterprise, sales_contact_id)

    console.print("[bold green]Le client a été ajouté avec succès ![/bold green]")

@with_db_session
def update_client_view(session):
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

        # Suite de la mise à jour...
        full_name = Prompt.ask("Entrez le nouveau nom complet du client", default=existing_client.full_name)
        email = Prompt.ask("Entrez le nouvel email du client", default=existing_client.email)
        phone = Prompt.ask("Entrez le nouveau téléphone du client", default=existing_client.phone)
        enterprise = Prompt.ask("Entrez le nouveau nom de l'entreprise du client", default=existing_client.enterprise)
        sales_contact_id = Prompt.ask("Entrez le nouvel ID du contact commercial", default=str(existing_client.sales_contact_id))

        # Validation de l'ID du contact commercial avant la mise à jour
        if not sales_contact_id.isdigit() or int(sales_contact_id) <= 0:
            console.print("[bold red]L'ID du contact commercial est invalide.[/bold red]")
            return

        # Appel de la méthode update_client du ClientController avec les nouvelles valeurs
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
    else:
        console.print(f"[bold red]Le client ID {client_id} n'a pas été trouvé.[/bold red]")



@with_db_session
def delete_client_view(session):
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
def show_clients(client_controller):
    clients = client_controller.list_clients()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")

    for client in clients:
        table.add_row(
            str(client.id),
            client.name,
            client.email,
            client.phone
        )

    console = Console()
    console.print(table)