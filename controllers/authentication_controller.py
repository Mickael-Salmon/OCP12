from accesscontrol.sec_sessions import create_session
from accesscontrol.functionnalities import login, logout
from models.user import UserSession, AuthenticationError, verify_credentials
from sqlalchemy.orm import Session

def verify_user_credentials(username, password):
    """
    Verify the user credentials.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        tuple: A tuple containing the user ID and the session token if the credentials are valid,
        otherwise (None, None).
    """
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

    Returns:
        None
    """
    with Session() as session:
        # Query the user_session by ID and delete it
        user_session = session.query(UserSession).get(session_id)
        if user_session:
            session.delete(user_session)
            session.commit()
