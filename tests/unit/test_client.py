import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from tests.factories.clientFactory import ClientFactory

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configurer la connexion à la base de données de test
DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def simple_client():
    return ClientFactory().create()

def test_client_creation(simple_client):
    assert simple_client.full_name != ""
    assert simple_client.email != ""
    assert "@" in simple_client.email
    assert simple_client.phone != ""
    assert simple_client.enterprise != ""
