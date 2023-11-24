from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from functools import wraps
from managers.manager import engine
# from models.user import UserSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import sentry_sdk

# Créer une session factory à utiliser pour obtenir une session
SessionFactory = sessionmaker(bind=engine)

def with_db_session(function):
    """
    Decorator to manage a database session for a given function.
    Handles session commit, rollback, and closure.

    Args:
        function: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        SQLAlchemyError: If an exception occurs during the execution of the function.
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        session = SessionFactory()
        try:
            result = function(session, *args, **kwargs)
            session.commit()  # Commit si aucune exception n'est levée
            return result
        except SQLAlchemyError as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            raise
        finally:
            session.close()
    return wrapper

@with_db_session
def create_session(session, user_id, jwt_token):
    """
    Creates a new user session in the database with the given JWT token.

    Args:
        session (Session): The database session.
        user_id (int): The ID of the user.
        jwt_token (str): The JWT token for the session.

    Returns:
        int: The ID of the created user session.
    """
    from models.user import UserSession
    new_user_session = UserSession(user_id=user_id, jwt_token=jwt_token)
    session.add(new_user_session)
    session.flush()  # Flush pour s'assurer que l'ID est généré si nécessaire
    return new_user_session.id

@with_db_session
def get_session(session, session_id):
    """
    Retrieves a user session from the database by ID.

    Args:
        session (Session): The database session.
        session_id (int): The ID of the user session.

    Returns:
        UserSession: The user session object if found, None otherwise.
    """
    from models.user import UserSession
    return session.query(UserSession).filter_by(id=session_id).first()

@with_db_session
def update_session_activity(session, session_id):
    """
    Updates the last activity timestamp of a user session.

    Args:
        session (Session): The database session.
        session_id (int): The ID of the user session.

    Returns:
        None
    """
    from models.user import UserSession
    user_session = session.query(UserSession).filter_by(id=session_id).first()
    if user_session:
        user_session.last_activity_at = func.now()

@with_db_session
def delete_session(session, session_id):
    """
    Deletes a user session from the database.

    Args:
        session (Session): The database session.
        session_id (int): The ID of the user session.
    """
    from models.user import UserSession
    user_session = session.query(UserSession).filter_by(id=session_id).first()
    if user_session:
        session.delete(user_session)

@with_db_session
def renew_session_jwt(session, session_id, new_jwt_token):
    """
    Renews the JWT token for an existing user session.

    Args:
        session (Session): The database session.
        session_id (int): The ID of the user session.
        new_jwt_token (str): The new JWT token for the session.

    Returns:
        bool: True if the token was successfully updated, False otherwise.
    """
    from models.user import UserSession
    user_session = session.query(UserSession).filter_by(id=session_id).first()
    if user_session:
        user_session.token = new_jwt_token
        user_session.expires_at = func.now() + timedelta(days=1)  # Update the expires_at time if needed
        return True
    return False
