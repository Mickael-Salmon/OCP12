import pytest
import os
from managers.contracts import ContractsManager
from factories.employeeFactory import EmployeeFactory
from factories.clientFactory import ClientFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from accesscontrol.jwt_token import create_token, store_token

# Charge les variables depuis le fichier .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

@pytest.fixture(scope='module')
def db_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Ceci retourne la session pour être utilisée dans les tests
    session.close()  # Ceci ferme la session une fois les tests terminés

@pytest.fixture
def setup_authenticated_environment(db_session):
    # Créer un utilisateur valide et récupérer son ID
    valid_user_id = 1  # Remplacer cette valeur par un id existant dans la BD

    # Créer un token JWT valide pour cet utilisateur
    token = create_token(user_id=valid_user_id)

    # Stocker ce token quelque part où tes fonctions pourront le retrouver
    store_token(token)

    yield  # Le `yield` signifie que le code après cette ligne sera exécuté après que les tests utilisant cette fixture soient terminés


@pytest.fixture
def setup_environment():
    # Initialisation de SQLAlchemy
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    factory = EmployeeFactory()
    employee = factory.create()  # Cette méthode renvoie une nouvelle instance de Employee
    client = ClientFactory()

    return employee, client, session


def test_create_contract(setup_environment, setup_authenticated_environment):
    employee, client, session = setup_environment

    # Insertion de l'employé dans la base de données
    session.add(employee)
    session.commit()
    employee_id = employee.id

    # Créer un token JWT avec cet ID
    token = create_token(user_id=employee_id)
    store_token(token)  # Stocke ce token pour qu'il soit utilisé dans les requêtes suivantes

    contracts_manager = ContractsManager(session)

    # Données pour créer un nouveau contrat
    client_id = client.id  # L'ID du client soit stocké dans client.id
    total_amount = 1000.0
    to_be_paid = 500.0
    is_signed = False

    # Créer le contrat et récupérer l'objet résultant
    new_contract = contracts_manager.create(
        client_id=client_id,
        total_amount=total_amount,
        to_be_paid=to_be_paid,
        is_signed=is_signed
    )

    # Vérifications
    assert new_contract is not None
    assert new_contract.client_id == client_id
    assert new_contract.total_amount == total_amount
    assert new_contract.to_be_paid == to_be_paid
    assert new_contract.is_signed == is_signed
