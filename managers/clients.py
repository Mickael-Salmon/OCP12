"""
This file defines the ClientsManager class, which serves as a manager for the 'Client' table in the database.
This class inherits from the base Manager class and extends it with functionalities and methods specific to managing clients.
It handles CRUD operations on clients and ensures that the user has the necessary permissions to perform certain actions, particularly through roles such as 'SALES'.
"""
import typing
from sqlalchemy.orm import Session
from database.manager import Manager
from models.clients import Client
from models.employees import Department as roles
from authentification.decorators import login_required, permission_required

class ClientsManager(Manager):
    """
    This class is responsible for handling the CRUD operations
    related to the `Client` model in the database.
    """

    def __init__(self, session: Session) -> None:
        """
        Constructor takes a SQLAlchemy session as an argument and initializes
        the parent class `Manager` with this session and the `Client` model.
        """
        super().__init__(session=session, model=Client)

    @permission_required(roles=[roles.SALES])
    def create(
        self,
        email: str,
        full_name: str,
        phone: str,
        enterprise: str,
        sales_contact_id: int,
    ) -> Client:
        """
        Creates a new record in the `Client` table. Takes multiple arguments like
        email, full_name, etc., to create a new instance of the `Client` model.
        Then uses the `create` method of the parent class `Manager` to perform
        the insert operation in the database.
        """
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=sales_contact_id,
        )
        return super().create(client)

    @login_required
    def get(self, *args, **kwargs) -> typing.List[Client]:
        """
        Retrieves records from the `Client` table based on the provided arguments
        and keywords. Calls the parent class `get` method.
        """
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Client]:
        """
        Retrieves all records from the `Client` table.
        """
        return super().all()

    @permission_required(roles=[roles.SALES])
    def update(self, *args, **kwargs):
        """
        Updates one or multiple records in the `Client` table.
        """
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        """
        Deletes one or multiple records from the `Client` table.
        """
        return super().delete(**kwargs)

    def filter_by_name(self, name_contains: str):
        """
        Custom function to filter records based on a name pattern.
        """
        return self.get(Client.full_name.contains(name_contains))