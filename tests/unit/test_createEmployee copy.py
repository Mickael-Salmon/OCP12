import pytest
from models.employees import Employee, Department
from models.clients import Client
from managers.clients import ClientsManager
from accesscontrol.jwt_token import create_token, store_token

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    user_id = 1  # ID de l'utilisateur pour les tests
    token = create_token(user_id)  # Créer un token JWT
    store_token(token)  # Stocker le token dans un fichier

@pytest.fixture
def simple_sales_employee() -> Employee:
    return Employee(
        full_name="John Sales",
        email="john.sales@epicevents.co",
        department=Department.SALES,
    )

@pytest.fixture
def account_employee() -> Employee:
    return Employee(
        full_name="Jane Accounting",
        email="jane.accounting@epicevents.co",
        department=Department.ACCOUNTING,
    )

@pytest.fixture
def simple_client() -> Client:
    return Client(
        email="client@test.test",
        full_name="Client, Test",
        phone="123456789",
        enterprise="TestCorp",
        sales_contact_id=1,
    )

def test_sales_employee_fixture(simple_sales_employee):
    assert simple_sales_employee.department == Department.SALES

def test_create_client_from_sales_employee(simple_sales_employee, simple_client):
    manager = ClientsManager(simple_sales_employee)

    # Filtrer les attributs non nécessaires
    valid_args = {k: v for k, v in simple_client.__dict__.items() if k not in ["_sa_instance_state"]}

    created_client = manager.create(**valid_args)

    assert created_client is not None
    assert created_client.email == simple_client.email

def test_create_client_from_account_employee_should_fail(account_employee, simple_client):
    manager = ClientsManager(account_employee)

    # Filtrer les attributs non nécessaires
    valid_args = {k: v for k, v in simple_client.__dict__.items() if k not in ["_sa_instance_state"]}

    with pytest.raises(PermissionError):
        manager.create(**valid_args)
