import pytest
import os
from sqlalchemy import create_engine
from accesscontrol.sec_sessions import Session, UserSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models.contracts import Contract
from tests.factories.contractFactory import ContractFactory

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configurer la connexion à la base de données de test
DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def simple_contract():
    return ContractFactory().create()

def test_contract_creation(simple_contract):
    assert simple_contract.total_amount > 0
    assert simple_contract.to_be_paid >= 0
