from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv
import bcrypt
import os
import psycopg2

# Création d'une instance de la console pour l'affichage
console = Console()

# Charger les variables d'environnement
load_dotenv()

# Informations de connexion à la base de données
DATABASE_URL = os.getenv('DATABASE_URL')

# Demande à l'utilisateur l'adresse email pour la réinitialisation du mot de passe
email_to_reset = Prompt.ask("[bold magenta]Entrez l'adresse email de l'utilisateur pour lequel vous souhaitez réinitialiser le mot de passe")

# Le nouveau mot de passe pour l'utilisateur spécifique
NEW_PASSWORD = Prompt.ask("[bold magenta]Entrez le nouveau mot de passe", password=True)

# Fonction pour hasher les mots de passe avec bcrypt
def hash_password(password):
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# Connexion à la base de données
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Sélectionne l'utilisateur avec l'email spécifié
cursor.execute("SELECT id FROM employees WHERE email = %s", (email_to_reset,))
user = cursor.fetchone()

if user:
    user_id = user[0]
    # Réinitialise le mot de passe avec bcrypt
    hashed_password = hash_password(NEW_PASSWORD)
    cursor.execute("UPDATE employees SET password_hash=%s WHERE id=%s;", (hashed_password, user_id))
    # Applique les changements
    conn.commit()
    console.print(f"[bold green]Le mot de passe pour {email_to_reset} a été réinitialisé avec succès.")
else:
    console.print("[bold red]Aucun utilisateur trouvé pour l'email spécifié.", style="red")

# Ferme la connexion
cursor.close()
conn.close()
