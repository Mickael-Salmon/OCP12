"""
This file defines the ContractsManager class, responsible for managing interactions with the 'Contract' table in the database.
The class extends the base Manager class, providing functionalities specific to contracts, such as CRUD operations.
It also includes permission checks to ensure that only authorized roles like 'ACCOUNTING' and 'SALES' can perform specific tasks like creating or updating contracts.
"""
import typing
from sqlalchemy.orm import Session
from managers.manager import Manager
from models.contracts import Contract
from models.employees import Department
from accesscontrol.sec_sessions import login_required, permission_required
from accesscontrol.jwt_token import get_authenticated_user_id

class ContractsManager(Manager):
    """
    Manages the operations related to the ``Contract`` table in the database.

    Inherits methods from the base Manager class to create, read, update, and delete contracts.
    Adds additional logic to handle specific rules and permissions.
    """
    def __init__(self, session: Session) -> None:
        """
        Initialize a ContractsManager instance.

        Args:
            session: SQLAlchemy session object.
        """
        super().__init__(session=session, model=Contract)

    @permission_required(roles=[Department.ACCOUNTING])
    def create(
        self, client_id: int, total_amount: float, to_be_paid: int, is_signed: bool
    ):
        """
        Create a new contract entry in the database.

        Requires accounting department permission.

        Args:
            client_id: The ID of the client associated with the contract.
            total_amount: The total amount of the contract.
            to_be_paid: The remaining amount to be paid.
            is_signed: Whether the contract is signed or not.

        Returns:
            The created Contract object.
        """
        return super().create(
            Contract(
                client_id=client_id,
                account_contact_id=get_authenticated_user_id(),
                total_amount=total_amount,
                to_be_paid=to_be_paid,
                is_signed=is_signed,
            )
        )

    @login_required
    def get(self, where_clause) -> typing.List[Contract]:
        """
        Retrieve a list of contracts based on the provided conditions.

        Requires user to be logged in.

        Args:
            where_clause: SQLAlchemy filter criteria.

        Returns:
            List of Contract objects that meet the conditions.
        """
        return super().get(where_clause)

    @login_required
    def all(self) -> typing.List[Contract]:
        """
        Retrieve all contracts from the database.

        Requires user to be logged in.

        Returns:
            List of all Contract objects.
        """
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, *args, **kwargs):
        """
        Update contract entries in the database.

        Requires either accounting or sales department permission.

        Args:
            *args: Positional arguments for updating.
            **kwargs: Keyword arguments for updating.

        Returns:
            None. Updates the Contract objects in the database.
        """
        return super().update(*args, **kwargs)

    def delete(*args, **kwargs):
        """
        Delete contract entries from the database.

        Args:
            *args: Positional arguments for deletion.
            **kwargs: Keyword arguments for deletion.

        Returns:
            None. Deletes the Contract objects from the database.
        """
        return super().delete(**kwargs)
