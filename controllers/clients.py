from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

class ClientController:
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_clients(self):
        return self.session.query(Client).all()

    def get_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if client:
            self.console.print(f"[bold green]Client trouvé :[/bold green] {client.full_name}")
        else:
            self.console.print("[bold red]Client non trouvé.[/bold red]")
        return client

    def create_client(self, full_name, email, phone, enterprise, sales_contact_id):
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
        active_contracts = self.session.query(Contract).filter(
            Contract.client_id == client_id,
            Contract.is_signed == True
        ).all()
        return len(active_contracts) > 0

    def search_clients(self, search_query):
        search = f"%{search_query}%"
        clients = self.session.query(Client).filter(
            or_(
                Client.full_name.ilike(search),
                Client.email.ilike(search)
            )
        ).all()
        return clients
