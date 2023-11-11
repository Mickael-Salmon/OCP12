from accesscontrol.sec_sessions import create_session
from accesscontrol.functionnalities import login, logout
from models.user import UserSession, AuthenticationError, verify_credentials
from sqlalchemy.orm import Session

def verify_user_credentials(username, password):
    try:
        # Vérifier les identifiants de l'utilisateur
        user = verify_credentials(username, password)
        if user:
            # Créer la session utilisateur et générer le JWT
            token = create_session(user.id)
            return user.id, token
    except AuthenticationError as error:
        print(str(error))  # Afficher ou gérer l'erreur comme il convient
    return None, None

def logout_user(session_id):
    """
    Log out the user by removing the session from user_sessions table.

    Args:
        session_id (int): The ID of the user session.
    """
    with Session() as session:
        # Query the user_session by ID and delete it
        user_session = session.query(UserSession).get(session_id)
        if user_session:
            session.delete(user_session)
            session.commit()
