﻿import typing
from sqlalchemy.orm import Session
from managers.manager import Manager
from models.events import Event
from models.employees import Department as roles
from accesscontrol.sec_sessions import permission_required

class EventsManager(Manager):
    """
    Manage the access to the `Event` table, serving as the business logic layer for CRUD operations.
    Extends the base Manager class and includes additional methods specific to the Event model.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the EventsManager with a database session and the Event model.

        Args:
            session (Session): The database session to be used.
        """
        super().__init__(session=session, model=Event)

    @permission_required(roles=[roles.SALES])
    def create(self, **kwargs) -> Event:
            """
            Create a new event record.
            Requires the user to have 'SALES' department privileges.

            Args:
                **kwargs: Keyword arguments containing the details of the event.

            Returns:
                Event: The newly created event object.

            """
            new_event = Event(**kwargs)
            return super().create(new_event)

    def get(self, *args, **kwargs) -> typing.List[Event]:
        """
        Retrieve one or more event records that match the given conditions.
        The user must be authenticated and have the required permissions to access the event data.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A list of Event objects that match the given conditions.
        """
        return super().get(*args, **kwargs)

    def all(self) -> typing.List[Event]:
        """
        Retrieve all event records from the database.
        The user must be authenticated and have the required permissions to access the event data.

        :return: A list of Event objects representing all the event records.
        """
        return super().all()

    @permission_required(roles=[roles.ACCOUNTING, roles.SUPPORT])
    def update(self, *args, **kwargs) -> Event:
        """
        Update one or more event records that match the given conditions.
        Requires the user to have 'ACCOUNTING' or 'SUPPORT' department privileges.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Event: The updated event record.

        """
        return super().update(*args, **kwargs)

    @permission_required(roles=[roles.ACCOUNTING, roles.SUPPORT])
    def delete(self, *args, **kwargs):
        """
        Delete one or more event records that match the given conditions.
        Requires the user to have 'ACCOUNTING' or 'SUPPORT' department privileges.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the delete operation.

        Raises:
            Any exceptions raised by the super().delete() method.
        """
        return super().delete(*args, **kwargs)
