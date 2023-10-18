from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from models import Base  # Assure-toi que tous tes modèles sont importés ici
from rich.console import Console

# Initialiser rich
console = Console()

# Charger les variables d'environnement
console.log("Chargement des variables d'environnement...", style="bold magenta")
load_dotenv()

# Récupérer l'URL de la base de données à partir des variables d'environnement
console.log("Récupération de l'URL de la base de données...", style="bold magenta")
database_url = os.getenv("DATABASE_URL")

# Créer une instance de 'engine' connectée à ta base de données PostgreSQL
console.log("Création de l'instance de 'engine'...", style="bold magenta")
engine = create_engine(database_url)

# Créer toutes les tables
console.log("Création des tables dans la base de données...", style="bold magenta")
Base.metadata.create_all(engine)

# Afficher un message de succès
console.log("Toutes les tables ont été créées avec succès!", style="bold green")
