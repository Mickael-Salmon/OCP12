from models.events import Event
from models.clients import Client
from models.employees import Employee
from rich.console import Console
from sqlalchemy import or_


class EventController:
    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_events(self):
        events = self.session.query(Event).all()
        self.console.print("[bold green]Liste des événements :[/bold green]")
        for event in events:
            client_name = event.client.full_name if event.client else "Client inconnu"
            self.console.print(f"ID: {event.id} | Client: {client_name} | Début: {event.start_date} | Fin: {event.end_date} | Lieu: {event.location}")
        return events

    def get_event(self, event_id):
        event = self.session.query(Event).get(event_id)
        if event:
            # Accède au nom du client via le contrat lié à l'événement
            client_name = event.contract.client.full_name if event.contract and event.contract.client else "Client inconnu"
            self.console.print(f"[bold green]Événement trouvé :[/bold green] ID {event.id} - {client_name}")
        else:
            self.console.print("[bold red]Événement non trouvé.[/bold red]")
        return event

    def create_event(self, start_date, end_date, location, attendees_count, notes, contract_id, support_contact_id):
        # Valider que l'employé existe
        support_contact = self.session.query(Employee).get(support_contact_id)
        if not support_contact:
            self.console.print(f"[bold red]Erreur : Aucun employé trouvé avec l'ID {support_contact_id}.[/bold red]")
            return None

        try:
            new_event = Event(
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees_count=attendees_count,
                notes=notes,
                contract_id=contract_id,
                support_contact_id=support_contact_id,  # Cet ID est validé
            )

            self.session.add(new_event)
            self.session.commit()
            self.console.print(f"[bold green]Événement créé avec succès ![/bold green]")
            return new_event
        except Exception as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création de l'événement : {e}[/bold red]")
            raise

    def update_event(self, event_id, **kwargs):
        event = self.session.query(Event).get(event_id)
        if event:
            for attr, value in kwargs.items():
                setattr(event, attr, value)
            self.session.commit()
            self.console.print(f"[bold green]Événement mis à jour : ID {event.id}[/bold green]")
            return event
        else:
            self.console.print("[bold red]Événement non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_event(self, event_id):
        event = self.session.query(Event).get(event_id)
        if event:
            self.session.delete(event)
            self.session.commit()
            self.console.print(f"[bold green]Événement supprimé : ID {event.id}[/bold green]")
        else:
            self.console.print("[bold red]Événement non trouvé pour suppression.[/bold red]")

    def search_events(self, search_query):
        if search_query.isdigit():
            # Recherche par ID de l'événement
            event_id = int(search_query)
            return self.session.query(Event).filter(Event.id == event_id).all()
        else:
            # Recherche par nom de client ou notes de l'événement
            search = f"%{search_query}%"
            return self.session.query(Event).join(Contract, Event.contract_id == Contract.id).join(Client, Contract.client_id == Client.id).filter(
                or_(Client.full_name.ilike(search), Event.notes.ilike(search))
            ).all()

