from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError

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
        new_contract = Contract(
            total_amount=total_amount,
            client_id=client_id,
            account_contact_id=account_contact_id,
            is_signed=False  # default value
        )
        self.session.add(new_contract)
        try:
            self.session.commit()
            self.console.print(f"[bold green]Contrat créé avec succès ![/bold green]")
            return new_contract
        except SQLAlchemyError as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création du contrat : {e}[/bold red]")
            raise

    def update_contract(self, contract_id, **kwargs):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            for attr, value in kwargs.items():
                setattr(contract, attr, value)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Contrat mis à jour : ID {contract.id}[/bold green]")
                return contract
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la mise à jour du contrat : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Contrat non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_contract(self, contract_id):
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            self.session.delete(contract)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Contrat supprimé : ID {contract.id}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la suppression du contrat : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Contrat non trouvé pour suppression.[/bold red]")

    def search_contracts(self, search_query):
        try:
            # Tente de convertir la recherche en un entier pour l'ID
            contract_id = int(search_query)
            return self.session.query(Contract).filter_by(id=contract_id).all()
        except ValueError:
            # Si ce n'est pas un entier, recherche par nom
            return self.session.query(Contract).join(Client).filter(
                or_(
                    Client.full_name.ilike(f"%{search_query}%")
                )
            ).all()
