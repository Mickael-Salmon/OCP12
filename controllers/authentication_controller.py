from models.user import verify_credentials
from utils.token_storage import clear_token

def verify_user_credentials(username, password):
    # Utilise le modèle pour vérifier les identifiants et obtenir le token
    return verify_credentials(username, password)

def logout_user():
    clear_token()  # Cette fonction doit effacer le token stocké
