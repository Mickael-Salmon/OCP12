from sqlalchemy.orm import Session
from managers.manager import Manager
from models.contracts import Contract
from models.employees import Department
from accesscontrol.sec_sessions import permission_required
from accesscontrol.jwt_token import get_authenticated_user_id
import typing

class ContractsManager(Manager):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Contract)

    @permission_required(roles=[Department.ACCOUNTING])
    def create(
        self, client_id: int, total_amount: float, to_be_paid: int, is_signed: bool
    ) -> Contract:
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
        return super().get(where_clause)

    def all(self) -> typing.List[Contract]:
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING, Department.SALES])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
