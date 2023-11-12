from factory import Factory, Sequence
from models.contracts import Contract

class ContractFactory(Factory):
    class Meta:
        model = Contract

    total_amount = 1000.00
    to_be_paid = 200.00
    is_signed = False
    client_id = 1
    account_contact_id = 1
