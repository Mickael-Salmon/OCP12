from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from accesscontrol.database_session import with_db_session
from controllers.events import EventController
from datetime import datetime
from rich.prompt import Prompt

console = Console()

def validate_date(date_str):
    """
    Validate a string in the format 'YYYY-MM-DD' and convert it to a datetime object.

    Args:
        date_str (str): The string to be validated and converted.

    Returns:
        datetime.date or None: The converted datetime object if the string is valid, None otherwise.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

@with_db_session
def list_events_view(session):
    """
    Display a table of events with their details.

    Args:
        session: The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Liste des événements[/bold cyan]")
    event_controller = EventController(session)
    events = event_controller.list_events()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Client")
    table.add_column("Début", justify="right")
    table.add_column("Fin", justify="right")
    table.add_column("Lieu")
    table.add_column("Participants", justify="right")

    for event in events:
        client_name = event.contract.client.full_name if event.contract and event.contract.client else "Client inconnu"
        start_date = event.start_date.strftime("%Y-%m-%d %H:%M")
        end_date = event.end_date.strftime("%Y-%m-%d %H:%M")
        table.add_row(
            str(event.id),
            client_name,
            start_date,
            end_date,
            event.location,
            str(event.attendees_count)
        )

    console.print(table)


@with_db_session
def add_event_view(session):
    """
    Displays a prompt to add a new event and collects information from the user.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Ajouter un nouvel événement[/bold cyan]")

    # Rest of the code...
def add_event_view(session):
    console.print("[bold cyan]Ajouter un nouvel événement[/bold cyan]")

    # Collecte et validation de la date de début
    start_date_str = Prompt.ask("Entrez la date de début de l'événement (YYYY-MM-DD)")
    start_date = validate_date(start_date_str)
    while start_date is None:
        console.print("[bold red]Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.[/bold red]")
        start_date_str = Prompt.ask("Entrez la date de début de l'événement (YYYY-MM-DD)")
        start_date = validate_date(start_date_str)

    # Collecte et validation de la date de fin
    end_date_str = Prompt.ask("Entrez la date de fin de l'événement (YYYY-MM-DD)")
    end_date = validate_date(end_date_str)
    while end_date is None:
        console.print("[bold red]Format de date invalide. Veuillez utiliser le format AAAA-MM-JJ.[/bold red]")
        end_date_str = Prompt.ask("Entrez la date de fin de l'événement (YYYY-MM-DD)")
        end_date = validate_date(end_date_str)
    location = Prompt.ask("Entrez le lieu de l'événement")
    attendees_count = Prompt.ask("Entrez le nombre de participants attendus", default="0")
    notes = Prompt.ask("Ajoutez des notes supplémentaires pour l'événement")
    contract_id = Prompt.ask("Entrez l'ID du contrat associé à l'événement")
    support_contact_id = Prompt.ask("Entrez l'ID du contact de support pour l'événement")

    # Convertir les valeurs si nécessaire, par exemple
    attendees_count = int(attendees_count)
    # Assure-toi que les IDs sont des entiers
    contract_id = int(contract_id)
    support_contact_id = int(support_contact_id)

    event_controller = EventController(session)
    event_controller.create_event(start_date, end_date, location, attendees_count, notes, contract_id, support_contact_id)

@with_db_session
def update_event_view(session):
    """
    Update an existing event with new information.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Modifier un événement existant[/bold cyan]")
    event_id = Prompt.ask("Entrez l'ID de l'événement à modifier")
    event_controller = EventController(session)
    existing_event = event_controller.get_event(event_id)

    if existing_event:
        # Récupérer et valider la nouvelle date de début
        new_start_date_str = Prompt.ask("Entrez la nouvelle date de début de l'événement (YYYY-MM-DD)", default=str(existing_event.start_date.date()))
        # Récupérer et valider la nouvelle date de fin
        new_end_date_str = Prompt.ask("Entrez la nouvelle date de fin de l'événement (YYYY-MM-DD)", default=str(existing_event.end_date.date()))
        # Récupérer le nouveau lieu de l'événement
        new_location = Prompt.ask("Entrez le nouveau lieu de l'événement", default=existing_event.location)
        # Récupérer le nouveau nombre de participants attendus
        new_attendees_count = Prompt.ask("Entrez le nouveau nombre de participants attendus", default=str(existing_event.attendees_count))
        # Récupérer les nouvelles notes supplémentaires pour l'événement
        new_notes = Prompt.ask("Ajoutez des notes supplémentaires pour l'événement", default=existing_event.notes)
        # Récupérer l'ID du contrat associé à l'événement
        new_contract_id = Prompt.ask("Entrez l'ID du contrat associé à l'événement", default=str(existing_event.contract_id))
        # Récupérer l'ID du contact de support pour l'événement
        new_support_contact_id = Prompt.ask("Entrez l'ID du contact de support pour l'événement", default=str(existing_event.support_contact_id))

        # Conversion des valeurs récupérées en types appropriés
        try:
            new_start_date = datetime.strptime(new_start_date_str, '%Y-%m-%d')
            new_end_date = datetime.strptime(new_end_date_str, '%Y-%m-%d')
            new_attendees_count = int(new_attendees_count)
            new_contract_id = int(new_contract_id)
            new_support_contact_id = int(new_support_contact_id)
        except ValueError as e:
            console.print(f"[bold red]Erreur de saisie : {e}[/bold red]")
            return

        # Appel de la méthode update_event du EventController avec les nouvelles valeurs
        updated_event = event_controller.update_event(
            event_id,
            start_date=new_start_date,
            end_date=new_end_date,
            location=new_location,
            attendees_count=new_attendees_count,
            notes=new_notes,
            contract_id=new_contract_id,
            support_contact_id=new_support_contact_id
        )

        if updated_event:
            console.print(f"[bold green]L'événement ID {event_id} a été modifié avec succès ![/bold green]")
        else:
            console.print(f"[bold red]Une erreur s'est produite lors de la mise à jour de l'événement.[/bold red]")
    else:
        console.print(f"[bold red]L'événement ID {event_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def delete_event_view(session):
    """
    Deletes an event based on the provided event ID.

    Args:
        session (Session): The session object for database connection.

    Returns:
        None
    """
    console.print("[bold cyan]Supprimer un événement[/bold cyan]")
    event_id = Prompt.ask("Entrez l'ID de l'événement à supprimer")
    event_controller = EventController(session)

    existing_event = event_controller.get_event(event_id)
    if existing_event:
        if Prompt.ask(f"Êtes-vous sûr de vouloir supprimer l'événement {existing_event.id}? (oui/non)", choices=["oui", "non"]) == "oui":
            event_controller.delete_event(event_id)
            console.print(f"[bold green]L'événement ID {event_id} a été supprimé avec succès ![/bold green]")
        else:
            console.print("[bold yellow]Suppression annulée.[/bold yellow]")
    else:
        console.print(f"[bold red]L'événement ID {event_id} n'a pas été trouvé.[/bold red]")

@with_db_session
def search_event_view(session):
    """
    Search for an event based on the provided ID or client name.

    Args:
        session (Session): The database session.

    Returns:
        None
    """
    console.print("[bold cyan]Rechercher un événement[/bold cyan]")
    search_query = Prompt.ask("Entrez l'ID de l'événement ou le nom du client à rechercher")
    # Création de l'instance de EventController
    event_controller = EventController(session)
    # Ici tu as besoin de déterminer si la recherche est par ID ou nom de client
    # Et puis effectuer la requête appropriée. Je vais supposer que tu as une méthode
    # dans event_controller pour gérer cela.

    events = event_controller.search_events(search_query)

    if events:
        for event in events:
            # Ici, nous accédons au client à travers la relation de contrat.
            client_name = event.contract.client.full_name if event.contract and event.contract.client else "Client inconnu"
            console.print(f"Événement trouvé : ID {event.id} - {client_name}")
    else:
        console.print("[bold red]Aucun événement trouvé avec cette recherche.[/bold red]")
