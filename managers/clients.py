from sqlalchemy.orm import Session
from managers.manager import Manager
from models.clients import Client
from models.employees import Department as roles
from accesscontrol.sec_sessions import permission_required
import typing

class ClientsManager(Manager):
    """
    Manager class for handling client operations.

    Args:
        session (Session): The database session.

    Attributes:
        session (Session): The database session.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Client)

    @permission_required(roles=[roles.SALES])
    def create(self, email: str, full_name: str, phone: str, enterprise: str, sales_contact_id: int) -> Client:
        """
        Create a new client.

        Args:
            email (str): The email address of the client.
            full_name (str): The full name of the client.
            phone (str): The phone number of the client.
            enterprise (str): The enterprise of the client.
            sales_contact_id (int): The ID of the sales contact associated with the client.

        Returns:
            Client: The created client object.
        """
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=sales_contact_id,
        )
        return super().create(client)

    def get(self, *args, **kwargs) -> typing.List[Client]:
        """
        Get clients based on specified filters.

        Returns:
            typing.List[Client]: A list of client objects.
        """
        return super().get(*args, **kwargs)

    def all(self) -> typing.List[Client]:
        """
        Get all clients.

        Returns:
            typing.List[Client]: A list of all client objects.
        """
        return super().all()

    @permission_required(roles=[roles.SALES])
    def update(self, *args, **kwargs):
        """
        Update clients based on specified filters.
        """
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete clients based on specified filters.
        """
        return super().delete(*args, **kwargs)

    def filter_by_name(self, name_contains: str):
        """
        Filter clients by name.

        Args:
            name_contains (str): The string to search for in the client names.
        """
        return self.get(Client.full_name.contains(name_contains))
