from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os
from models.employees import Employee  # Remplacer par tes modèles
from models.clients import Client
from models.contracts import Contract
from models.events import Event
from database.database import Session


# Load Environment variables
load_dotenv()

# Get the database url from environment variables
database_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(database_url, echo=True)

session = Session()  # Remplacer par la manière dont tu initialises ta session SQLAlchemy

# Vider les tables
session.query(Employee).delete()
session.query(Client).delete()
session.query(Contract).delete()
session.query(Event).delete()

# Valider les changements
session.commit()

print("Toutes les tables ont été vidées.")