from models.contracts import Contract
from models.employees import Employee
from models.clients import Client
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

class ContractFactory:
    def __init__(self):
        self.total_amount = fake.random_number(digits=5)
        self.to_be_paid = fake.random_number(digits=4)
        self.client_id = 4
        self.account_contact_id = 6

    def create(self):
        contract = Contract(
            total_amount=self.total_amount,
            to_be_paid=self.to_be_paid,
            client_id=self.client_id,
            account_contact_id=self.account_contact_id,
            is_signed=fake.boolean()
        )
        return contract
