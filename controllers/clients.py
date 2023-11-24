from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

class ClientController:
    """
    The ClientController class handles operations related to clients in the system.

    Attributes:
        session (Session): The database session object.
        console (Console): The console object for printing messages.

    Methods:
        list_clients(): Retrieve a list of all clients.
        get_client(client_id): Retrieve a client by its ID.
        create_client(full_name, email, phone, enterprise, sales_contact_id): Create a new client.
        update_client(client_id, **kwargs): Update a client's information.
        delete_client(client_id): Delete a client.
        deactivate_client(client_id): Deactivate a client.
        has_active_contracts(client_id): Check if a client has active contracts.
        search_clients(search_query): Search for clients based on a search query.
    """
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_clients(self):
        """
        Retrieve a list of all clients.

        Returns:
            list: A list of Client objects representing the clients.
        """
        return self.session.query(Client).all()

    def get_client(self, client_id):
        """
        Retrieve a client by its ID.

        Args:
            client_id (int): The ID of the client.

        Returns:
            Client: The Client object representing the client, or None if not found.
        """
        client = self.session.query(Client).get(client_id)
        if client:
            self.console.print(f"[bold green]Client trouvé :[/bold green] {client.full_name}")
        else:
            self.console.print("[bold red]Client non trouvé.[/bold red]")
        return client

    def create_client(self, full_name, email, phone, enterprise, sales_contact_id):
        """
        Create a new client.

        Args:
            full_name (str): The full name of the client.
            email (str): The email address of the client.
            phone (str): The phone number of the client.
            enterprise (str): The enterprise of the client.
            sales_contact_id (int): The ID of the sales contact associated with the client.

        Returns:
            Client: The newly created Client object.
        """
        new_client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=sales_contact_id
        )
        self.session.add(new_client)
        try:
            self.session.commit()
            self.console.print(f"[bold green]Client {full_name} créé avec succès ![/bold green]")
        except SQLAlchemyError as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création du client : {e}[/bold red]")
            raise
        return new_client

    def update_client(self, client_id, **kwargs):
        """
        Update a client's information.

        Args:
            client_id (int): The ID of the client.
            **kwargs: Keyword arguments representing the attributes to update.

        Returns:
            Client: The updated Client object, or None if the client was not found.
        """
        client = self.session.query(Client).get(client_id)
        if client:
            for attr, value in kwargs.items():
                setattr(client, attr, value)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Client mis à jour : {client.full_name}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la mise à jour du client : {e}[/bold red]")
                raise
            return client
        else:
            self.console.print("[bold red]Client non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_client(self, client_id):
        """
        Delete a client.

        Args:
            client_id (int): The ID of the client.
        """
        client = self.session.query(Client).get(client_id)
        if client:
            self.session.delete(client)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Client supprimé : {client.full_name}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la suppression du client : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Client non trouvé pour suppression.[/bold red]")

    def deactivate_client(self, client_id):
        """
        Deactivate a client.

        Args:
            client_id (int): The ID of the client.
        """
        client = self.session.query(Client).get(client_id)
        if client:
            client.is_active = False
            try:
                self.session.commit()
                self.console.print(f"[bold green]Client désactivé : {client.full_name}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la désactivation du client : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Client non trouvé pour désactivation.[/bold red]")

    def has_active_contracts(self, client_id):
        """
        Check if a client has active contracts.

        Args:
            client_id (int): The ID of the client.

        Returns:
            bool: True if the client has active contracts, False otherwise.
        """
        active_contracts = self.session.query(Contract).filter(
            Contract.client_id == client_id,
            Contract.is_signed == True
        ).all()
        return len(active_contracts) > 0

    def search_clients(self, search_query):
        """
        Search for clients based on a search query.

        Args:
            search_query (str): The search query.

        Returns:
            list: A list of Client objects matching the search query.
        """
        search = f"%{search_query}%"
        clients = self.session.query(Client).filter(
            or_(
                Client.full_name.ilike(search),
                Client.email.ilike(search)
            )
        ).all()
        return clients
