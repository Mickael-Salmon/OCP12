from sqlalchemy.orm import Session
from managers.manager import Manager
from models.clients import Client
from models.employees import Department as roles
from accesscontrol.sec_sessions import permission_required
import typing

class ClientsManager(Manager):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session, model=Client)

    @permission_required(roles=[roles.SALES])
    def create(self, email: str, full_name: str, phone: str, enterprise: str, sales_contact_id: int) -> Client:
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            enterprise=enterprise,
            sales_contact_id=sales_contact_id,
        )
        return super().create(client)

    def get(self, *args, **kwargs) -> typing.List[Client]:
        return super().get(*args, **kwargs)

    def all(self) -> typing.List[Client]:
        return super().all()

    @permission_required(roles=[roles.SALES])
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def filter_by_name(self, name_contains: str):
        return self.get(Client.full_name.contains(name_contains))
