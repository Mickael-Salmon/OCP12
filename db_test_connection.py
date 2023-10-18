from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données
database_url = os.getenv("DATABASE_URL")

# Créer un moteur de base de données
engine = create_engine(database_url, echo=True)

# Test de connexion
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Connection successful:", result.fetchone()[0] == 1)

