from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer l'URL de la base de données depuis les variables d'environnement
database_url = os.getenv("DATABASE_URL")

# Créer l'engine de la base de données
engine = create_engine(database_url, echo=True)  # Mettre echo à False pour annuler les logs

# Créer une classe de session liée à cet engine
Session = sessionmaker(bind=engine)
