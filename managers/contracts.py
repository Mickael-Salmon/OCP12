from sqlalchemy.orm import Session
from managers.manager import Manager
from models.contracts import Contract
from models.employees import Department
from accesscontrol.sec_sessions import permission_required
from accesscontrol.jwt_token import get_authenticated_user_id
import typing

class ContractsManager(Manager):
    """
    Manager class for handling contracts.

    Args:
        session (Session): The database session.

    Attributes:
        session (Session): The database session.

    Methods:
        create: Create a new contract.
        get: Retrieve contracts based on a where clause.
        all: Retrieve all contracts.
        update: Update contracts.
        delete: Delete contracts.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Contract)

    @permission_required(roles=[Department.ACCOUNTING])
    def create(
        self, client_id: int, total_amount: float, to_be_paid: int, is_signed: bool
    ) -> Contract:
        """
        Create a new contract.

        Args:
            client_id (int): The ID of the client.
            total_amount (float): The total amount of the contract.
            to_be_paid (int): The amount to be paid.
            is_signed (bool): Indicates if the contract is signed.

        Returns:
            Contract: The created contract.
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

    def get(self, where_clause) -> typing.List[Contract]:
        """
        Retrieve contracts based on a where clause.

        Args:
            where_clause: The where clause to filter contracts.

        Returns:
            List[Contract]: The list of contracts matching the where clause.
        """
        return super().get(where_clause)

    def all(self) -> typing.List[Contract]:
        """
        Retrieve all contracts.

        Returns:
            List[Contract]: The list of all contracts.
        """
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, *args, **kwargs):
        """
        Update contracts.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the update operation.
        """
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete contracts.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the delete operation.
        """
        return super().delete(*args, **kwargs)
