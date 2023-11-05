from models.clients import Client
from models.contracts import Contract
from rich.console import Console
from sqlalchemy import or_


class ClientController:
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_clients(self):
        clients = self.session.query(Client).all()
        self.console.print("[bold green]Liste des clients :[/bold green]")
        for client in clients:
            self.console.print(f"{client.id} : {client.full_name} - {client.email}")
        return clients

    def get_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if client:
            self.console.print(f"[bold green]Client trouvé :[/bold green] {client.full_name}")
        else:
            self.console.print("[bold red]Client non trouvé.[/bold red]")
        return client

    def create_client(self, full_name, email, phone, enterprise, sales_contact_id):
        try:
            new_client = Client(
                full_name=full_name,
                email=email,
                phone=phone,
                enterprise=enterprise,
                sales_contact_id=sales_contact_id
            )
            self.session.add(new_client)
            self.session.commit()
            self.console.print(f"[bold green]Client {full_name} créé avec succès ![/bold green]")
            return new_client
        except Exception as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création du client : {e}[/bold red]")
            raise

    # def update_client(self, client_id, **kwargs):
    #     client = self.session.query(Client).get(client_id)
    #     if client:
    #         for attr, value in kwargs.items():
    #             setattr(client, attr, value)
    #         self.session.commit()
    #         self.console.print(f"[bold green]Client mis à jour : {client.full_name}[/bold green]")
    #         return client
    #     else:
    #         self.console.print("[bold red]Client non trouvé pour mise à jour.[/bold red]")
    #         return None

    # def update_client(self, client_id, **kwargs):
    #     client = self.session.query(Client).get(client_id)
    #     if client:
    #         for attr, value in kwargs.items():
    #             setattr(client, attr, value)
    #         self.session.commit()
    #         self.console.print(f"[bold green]Client mis à jour : {client.full_name}[/bold green]")
    #         return client
    #     else:
    #         self.console.print("[bold red]Client non trouvé pour mise à jour.[/bold red]")
    #     return None
    def update_client(self, client_id, **kwargs):
        client = self.session.query(Client).get(client_id)
        if client:
            for attr, value in kwargs.items():
                setattr(client, attr, value)
            self.session.commit()
            self.console.print(f"[bold green]Client mis à jour : {client.full_name}[/bold green]")
            return client
        else:
            self.console.print("[bold red]Client non trouvé pour mise à jour.[/bold red]")
        return None

    def delete_client(self, client_id):
        client = self.session.query(Client).get(client_id)
        if client:
            self.session.delete(client)
            self.session.commit()
            self.console.print(f"[bold green]Client supprimé : {client.full_name}[/bold green]")
        else:
            self.console.print("[bold red]Client non trouvé pour suppression.[/bold red]")

    def deactivate_client(self, client_id):
        """
        Désactive un client en mettant à jour son statut is_active à False.

        Args:
        * client_id (int): L'identifiant du client.
        """
        client = self.session.query(Client).get(client_id)
        if client:
            client.is_active = False
            self.session.commit()
            self.console.print(f"[bold green]Client désactivé : {client.full_name}[/bold green]")
        else:
            self.console.print("[bold red]Client non trouvé pour désactivation.[/bold red]")

    def has_active_contracts(self, client_id):
        """
        Vérifie si le client a des contrats actifs.

        Args:
        * client_id (int): L'identifiant du client.

        Returns:
        * bool: True si le client a des contrats actifs, False autrement.
        """
        # Ici, on vérifie l'état de signature des contrats pour déterminer s'ils sont actifs
        active_contracts = self.session.query(Contract).filter(
            Contract.client_id == client_id,
            Contract.is_signed == True
        ).all()
        return len(active_contracts) > 0

    def search_clients(self, search_query):
        search = f"%{search_query}%"
        return self.session.query(Client).filter(
            or_(
                Client.full_name.ilike(search),
                Client.email.ilike(search)
            )
        ).all()