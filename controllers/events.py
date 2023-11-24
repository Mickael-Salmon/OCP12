from models.events import Event
from models.clients import Client
from models.contracts import Contract
from models.employees import Employee
from rich.console import Console
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

class EventController:
    """
    Controller class for managing events.
    """

    def __init__(self, session):
        self.session = session
        self.console = Console()

    def list_events(self):
        """
        Retrieve a list of all events.

        Returns:
            list: A list of Event objects representing the events.
        """
        return self.session.query(Event).all()

    def get_event(self, event_id):
        """
        Retrieve an event by its ID.

        Args:
            event_id (int): The ID of the event to retrieve.

        Returns:
            Event: The Event object representing the event, or None if not found.
        """
        event = self.session.query(Event).get(event_id)
        if event:
            client_name = event.contract.client.full_name if event.contract and event.contract.client else "Client inconnu"
            self.console.print(f"[bold green]Événement trouvé :[/bold green] ID {event.id} - {client_name}")
        else:
            self.console.print("[bold red]Événement non trouvé.[/bold red]")
        return event

    def create_event(self, start_date, end_date, location, attendees_count, notes, contract_id, support_contact_id):
        """
        Create a new event.

        Args:
            start_date (datetime): The start date of the event.
            end_date (datetime): The end date of the event.
            location (str): The location of the event.
            attendees_count (int): The number of attendees for the event.
            notes (str): Additional notes for the event.
            contract_id (int): The ID of the contract associated with the event.
            support_contact_id (int): The ID of the support contact for the event.

        Returns:
            Event: The Event object representing the newly created event, or None if an error occurred.
        """
        support_contact = self.session.query(Employee).get(support_contact_id)
        if not support_contact:
            self.console.print(f"[bold red]Erreur : Aucun employé trouvé avec l'ID {support_contact_id}.[/bold red]")
            return None

        new_event = Event(
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees_count=attendees_count,
            notes=notes,
            contract_id=contract_id,
            support_contact_id=support_contact_id
        )

        self.session.add(new_event)
        try:
            self.session.commit()
            self.console.print("[bold green]Événement créé avec succès ![/bold green]")
            return new_event
        except SQLAlchemyError as e:
            self.session.rollback()
            self.console.print(f"[bold red]Erreur lors de la création de l'événement : {e}[/bold red]")
            raise

    def update_event(self, event_id, **kwargs):
        """
        Update an existing event.

        Args:
            event_id (int): The ID of the event to update.
            **kwargs: Keyword arguments representing the attributes to update.

        Returns:
            Event: The Event object representing the updated event, or None if not found.
        """
        event = self.session.query(Event).get(event_id)
        if event:
            for attr, value in kwargs.items():
                setattr(event, attr, value)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Événement mis à jour : ID {event.id}[/bold green]")
                return event
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la mise à jour de l'événement : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Événement non trouvé pour mise à jour.[/bold red]")
            return None

    def delete_event(self, event_id):
        """
        Delete an event.

        Args:
            event_id (int): The ID of the event to delete.
        """
        event = self.session.query(Event).get(event_id)
        if event:
            self.session.delete(event)
            try:
                self.session.commit()
                self.console.print(f"[bold green]Événement supprimé : ID {event.id}[/bold green]")
            except SQLAlchemyError as e:
                self.session.rollback()
                self.console.print(f"[bold red]Erreur lors de la suppression de l'événement : {e}[/bold red]")
                raise
        else:
            self.console.print("[bold red]Événement non trouvé pour suppression.[/bold red]")

    def search_events(self, search_query):
        """
        Search events based on a search query.

        Args:
            search_query (str): The search query to match against event names and notes.

        Returns:
            list: A list of Event objects matching the search query.
        """
        search = f"%{search_query}%"
        events = self.session.query(Event).join(Contract, Event.contract_id == Contract.id).join(Client, Contract.client_id == Client.id).filter(
            or_(Client.full_name.ilike(search), Event.notes.ilike(search))
        ).all()
        return events
