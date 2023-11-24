from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from accesscontrol.database_session import with_db_session
from controllers.contracts import ContractController
from models.contracts import Contract

console = Console()

@with_db_session
def list_contracts_view(session):
    """
    Display a table of contracts with their details.

    Args:
        session: The database session object.

    Returns:
        None
    """
    console.print("[bold cyan]Liste des contrats[/bold cyan]")
    contracts = session.query(Contract).all()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Client")
    table.add_column("Montant total", justify="right")
    table.add_column("À payer", justify="right")
    table.add_column("Signé")

    for contract in contracts:
        client_name = contract.client.full_name if contract.client else "Client inconnu"
        signed_status = "Oui" if contract.is_signed else "Non"
        table.add_row(
            str(contract.id),
            client_name,
            f"{contract.total_amount:.2f} €",
            f"{contract.to_be_paid:.2f} €",
            signed_status
        )

    console.print(table)


@with_db_session
def add_contract_view(user_id, token, session):
    """
    Displays a view for adding a new contract.

    Args:
        user_id (int): The ID of the user.
        token (str): The authentication token.
        session: The session object for database operations.

    Returns:
        None
    """
    console.print("[bold cyan]Ajouter un nouveau contrat[/bold cyan]")
    total_amount = Prompt.ask("Entrez le montant total du contrat")
    client_id = Prompt.ask("Entrez l'ID du client pour le contrat")
    account_contact_id = Prompt.ask("Entrez l'ID du contact commercial")

    # Ici, on pourrait ajouter des validations pour les IDs et les montants

    contract_controller = ContractController(session)
    contract_controller.create_contract(total_amount, client_id, account_contact_id)

    console.print("[bold green]Le contrat a été ajouté avec succès ![/bold green]")

@with_db_session
def update_contract_view(session):
    """
    Updates an existing contract.

    Args:
        session: The session object.

    Returns:
        None
    """
    console.print("[bold cyan]Modifier un contrat existant[/bold cyan]")
    contract_id = Prompt.ask("Entrez l'ID du contrat à modifier")
    contract_controller = ContractController(session)
    existing_contract = contract_controller.get_contract(contract_id)

    if existing_contract:
        try:
            # Demande le nouveau montant total du contrat et le convertit en float
            total_amount = float(Prompt.ask("Entrez le nouveau montant total du contrat", default=str(existing_contract.total_amount)))
            is_signed_str = Prompt.ask("Le contrat est-il signé ? (oui/non)", choices=["oui", "non"])

            # Conversion de la réponse en booléen
            is_signed = True if is_signed_str.lower() == 'oui' else False

            # Appel de la méthode update_contract du ContractController avec les nouvelles valeurs
            updated_contract = contract_controller.update_contract(contract_id,
                                                                total_amount=total_amount,
                                                                is_signed=is_signed)

            if updated_contract:
                console.print(f"[bold green]Le contrat ID {contract_id} a été modifié avec succès ![/bold green]")
            else:
                console.print(f"[bold red]Une erreur s'est produite lors de la mise à jour du contrat.[/bold red]")
        except ValueError as e:
            console.print(f"[bold red]Erreur : {e}[/bold red]")
    else:
        console.print(f"[bold red]Le contrat ID {contract_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def delete_contract_view(session):
    """
    Displays a prompt to delete a contract based on its ID.
    If the contract exists, it asks for confirmation before deleting it.
    If confirmed, the contract is deleted and a success message is displayed.
    If not confirmed or the contract doesn't exist, appropriate messages are displayed.

    Args:
        session: The session object for database connection.
    """
    console.print("[bold cyan]Supprimer un contrat[/bold cyan]")
    contract_id = Prompt.ask("Entrez l'ID du contrat à supprimer")
    contract_controller = ContractController(session)

    existing_contract = contract_controller.get_contract(contract_id)
    if existing_contract:
        if Prompt.ask(f"Êtes-vous sûr de vouloir supprimer le contrat {existing_contract.id}? (oui/non)", choices=["oui", "non"]) == "oui":
            contract_controller.delete_contract(contract_id)
            console.print(f"[bold green]Le contrat ID {contract_id} a été supprimé avec succès ![/bold green]")
        else:
            console.print("[bold yellow]Suppression annulée.[/bold yellow]")
    else:
        console.print(f"[bold red]Le contrat ID {contract_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def search_contract_view(session):
    """
    Search for a contract based on the provided search query.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Rechercher un contrat[/bold cyan]")
    search_query = Prompt.ask("Entrez l'ID du contrat ou le nom du client à rechercher")

    contract_controller = ContractController(session)
    contracts = contract_controller.search_contracts(search_query)

    if contracts:
        console.print("[bold green]Contrats trouvés :[/bold green]")
        for contract in contracts:
            console.print(f"ID: {contract.id} | Client: {contract.client.full_name} | Montant: {contract.total_amount} | Signé: {'Oui' if contract.is_signed else 'Non'}")
    else:
        console.print("[bold red]Aucun contrat correspondant à la recherche.[/bold red]")
