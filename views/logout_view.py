from controllers.authentication_controller import logout_user
from accesscontrol.jwt_token import decode_token
from accesscontrol.sec_sessions import get_current_user_token

def logout_view(token):
    # Récupérer le token JWT de la session actuelle
    token = get_current_user_token()
    if token:
        # Utiliser decode_token pour obtenir l'ID de l'utilisateur du token
        user_id = decode_token(token)
        if user_id:
            # Appeler la fonction logout_user avec l'ID de l'utilisateur pour terminer la session
            logout_user(user_id)
            print("Vous avez été déconnecté.")
        else:
            print("La déconnexion a échoué, token invalide.")
    else:
        print("Aucune session active trouvée.")
