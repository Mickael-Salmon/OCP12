from controllers.authentication_controller import verify_user_credentials
from utils.token_storage import save_token

def login_view():
    # Demande à l'utilisateur son nom d'utilisateur et son mot de passe
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")
    # Appelle le contrôleur pour vérifier ces informations
    token = verify_user_credentials(username, password)
    if token:
        # Si authentification réussie, sauvegarde le token
        save_token(token)
        print("Connexion réussie.")
    else:
        print("Identifiants incorrects.")
