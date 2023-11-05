from factory import Factory, Sequence
from models.clients import Client

class ClientFactory(Factory):
    class Meta:
        model = Client

    full_name = Sequence(lambda n: f"Jane Client {n}")
    email = Sequence(lambda n: f"jane.client{n}@epicevents.co")
    phone = Sequence(lambda n: f"01234567{n}")
    enterprise = "Epic Enterprise"
    sales_contact_id = 1 # We could use EMployeeFactory here if needed
