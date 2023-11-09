from models.user import verify_credentials
from utils.token_storage import clear_token

def verify_user_credentials(username, password):
    # Utilise le modèle pour vérifier les identifiants
    user, token = verify_credentials(username, password)
    if user and token:
        # Retourne l'ID de l'utilisateur et le token si les identifiants sont corrects
        return user.id, token
    else:
        # Retourne None, None si les identifiants sont incorrects
        return None, None

def logout_user():
    clear_token()  # Cette fonction doit effacer le token stocké
