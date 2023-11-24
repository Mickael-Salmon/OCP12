from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from rich.table import Table
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError

class ContractController:
    """
    Controller class for managing contracts.
    """

    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_contracts(self):
        """
        Retrieve a list of all contracts.

        Returns:
            list: A list of Contract objects.
        """
        return self.session.query(Contract).all()

    def get_contract(self, contract_id):
        """
        Retrieve a contract by its ID.

        Args:
            contract_id (int): The ID of the contract.

        Returns:
            Contract: The Contract object if found, None otherwise.
        """
        contract = self.session.query(Contract).get(contract_id)
        if contract:
            client_name = contract.client.full_name if contract.client else "Client inconnu"
            self.console.print(f"[bold green]Contrat trouvé :[/bold green] ID {contract.id} - {client_name}")
        else:
            self.console.print("[bold red]Contrat non trouvé.[/bold red]")
        return contract

    def create_contract(self, total_amount, to_be_paid, client_id, account_contact_id):
        """
        Create a new contract.

        Args:
            total_amount (float): The total amount of the contract.
            client_id (int): The ID of the client associated with the contract.
            account_contact_id (int): The ID of the account contact associated with the contract.

        Returns:
            Contract: The newly created Contract object.
        """
        new_contract = Contract(
            total_amount=total_amount,
            to_be_paid=to_be_paid,
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
        """
        Update a contract.

        Args:
            contract_id (int): The ID of the contract.
            **kwargs: Keyword arguments representing the attributes to be updated.

        Returns:
            Contract: The updated Contract object if found, None otherwise.
        """
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
        """
        Delete a contract.

        Args:
            contract_id (int): The ID of the contract.
        """
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
        """
        Search contracts by ID or client name.

        Args:
            search_query (str): The search query.

        Returns:
            list: A list of Contract objects matching the search query.
        """
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
