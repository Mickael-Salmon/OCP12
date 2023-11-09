from controllers.authentication_controller import verify_user_credentials
from utils.token_storage import save_token

def login_view():
    # Demande à l'utilisateur son nom d'utilisateur et son mot de passe
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")
    # Appelle le contrôleur pour vérifier ces informations
    employee_id, token = verify_user_credentials(username, password)
    if token and employee_id:
        # Si authentification réussie, sauvegarde le token avec l'ID de l'employé
        save_token(employee_id, token)
        print("Connexion réussie.")
    else:
        print("Identifiants incorrects.")
