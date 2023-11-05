from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from sqlalchemy import or_, and_


class ContractController:
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_contracts(self):
        contracts = self.session.query(Contract).all()
        self.console.print("[bold green]Liste des contrats :[/bold green]")
        for contract in contracts:
            client_name = contract.client.full_name if contract.client else "Client inconnu"
            self.console.print(f"{contract.id} : {client_name} - {contract.total_amount} - {'Signé' if contract.is_signed else 'Non signé'}")
        return contracts

    def get_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            client_name = contract.client.full_name if contract.client else "Client inconnu"
            self.console.print(f"[bold green]Contrat trouvé :[/bold green] ID {contract.id} - {client_name}")
        else:
            self.console.print("[bold red]Contrat non trouvé.[/bold red]")
        return contract

    def create_contract(self, total_amount, client_id, account_contact_id):
        try:
            new_contract = Contract(
                total_amount=total_amount,
                client_id=client_id,
                account_contact_id=account_contact_id,
                is_signed=False  # default value
            )
            self.session.add(new_contract)
            self.session.commit()
            self.console.print(f"[bold green]Contrat créé avec succès ![/bold green]")
            return new_contract
        except Exception as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création du contrat : {e}[/bold red]")
            raise

    def update_contract(self, contract_id, **kwargs):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            for attr, value in kwargs.items():
                setattr(contract, attr, value)
            self.session.commit()
            self.console.print(f"[bold green]Contrat mis à jour : ID {contract.id}[/bold green]")
            return contract
        else:
            self.console.print("[bold red]Contrat non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            self.session.delete(contract)
            self.session.commit()
            self.console.print(f"[bold green]Contrat supprimé : ID {contract.id}[/bold green]")
        else:
            self.console.print("[bold red]Contrat non trouvé pour suppression.[/bold red]")

    def search_contracts(self, search_query):
        if search_query.isdigit():  # Si la recherche est un nombre, on cherche par ID.
            contract_id = int(search_query)
            return self.session.query(Contract).filter(Contract.id == contract_id).all()
        else:  # Sinon, on cherche par nom en utilisant ILIKE.
            search = f"%{search_query}%"
            return self.session.query(Contract).join(Client).filter(
                Client.full_name.ilike(search)
        ).all()

