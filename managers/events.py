"""
This file defines the EventsManager class which serves as the business logic layer for the 'Event' model.
It extends the base Manager class and includes methods for CRUD operations on the 'Event' table.
The class includes methods to create, read, update, and delete Event records, making sure that the right permissions are checked before performing certain operations.
"""
import typing
from sqlalchemy.orm import Session
from managers.manager import Manager
from models.events import Event
from models.employees import Department as roles
from accesscontrol.sec_sessions import login_required, permission_required


class EventsManager(Manager):
    """
    Manage the access to the ``Event`` table, serving as the business logic layer for CRUD operations.
    Extends the base Manager class and includes additional methods specific to the Event model.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the EventsManager with a database session and the Event model.
        """
        super().__init__(session=session, model=Event)

    @permission_required([roles.SALES])
    def create(self, *args, **kwargs):
        """
        Create a new event record.
        Requires the user to have 'SALES' department privileges.
        """
        return super().create(**kwargs)

    @login_required
    def get(self, *args, **kwargs):
        """
        Retrieve one or more event records that match the given conditions.
        Requires the user to be logged in.
        """
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Event]:
        """
        Retrieve all event records from the database.
        Requires the user to be logged in.
        """
        return super().all()

    @permission_required([roles.ACCOUNTING, roles.SUPPORT])
    def update(self, *args, **kwargs):
        """
        Update one or more event records that match the given conditions.
        Requires the user to have 'ACCOUNTING' or 'SUPPORT' department privileges.
        """
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete one or more event records that match the given conditions.
        """
        return super().delete(**kwargs)
