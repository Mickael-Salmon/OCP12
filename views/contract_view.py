from rich.prompt import Prompt
from rich.console import Console
from accesscontrol.database_session import with_db_session
from controllers.contracts import ContractController

console = Console()

@with_db_session
def list_contracts_view(session):
    console.print("[bold cyan]Liste des contrats[/bold cyan]")
    contract_controller = ContractController(session)
    contract_controller.list_contracts()

@with_db_session
def add_contract_view(user_id, token, session):
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
