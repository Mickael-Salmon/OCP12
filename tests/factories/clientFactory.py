from factory import Factory, Sequence
from models.clients import Client
from models.employees import Employee
from accesscontrol.sec_sessions import Session, UserSession
from faker import Faker
from datetime import datetime

fake = Faker()

class ClientFactory:
    def __init__(self):
        self.full_name = fake.name()
        self.email = f"{fake.email().split('@')[0]}+{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        self.phone = fake.phone_number()
        self.enterprise = fake.company()

    def create(self):
        client = Client(
            full_name=self.full_name,
            email=self.email,
            phone=self.phone,
            enterprise=self.enterprise
        )
        return client

