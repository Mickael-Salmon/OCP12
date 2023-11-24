"""
This file contains security decorators for the application, ensuring authenticated
and authorized access to certain functions or routes based on user roles.
"""

from sqlalchemy.orm import Session
from models.employees import Employee, Department
from managers.manager import engine
from accesscontrol.jwt_token import decode_token
from models.user import UserSession
from accesscontrol.env_variables import SECRET_KEY
from functools import wraps
from accesscontrol.load_current_user import load_current_user
from sqlalchemy.orm import sessionmaker


def authenticated_action(function):
    """
    Decorator function that performs authentication before executing the decorated function.

    Args:
        function (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    Raises:
        PermissionError: If the JWT token is missing, invalid, or the user is not authenticated.
    """
    def wrapper(*args, **kwargs):
        """
        A decorator function that performs authentication and authorization checks using a JWT token.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function.

        Raises:
            PermissionError: If the JWT token is missing, invalid, or the user is not authenticated.
        """
        session = Session(engine)
        token = kwargs.get('token')  # Assumons que le token JWT est passé dans kwargs
        if token is None:
            raise PermissionError("JWT token is required for authentication.")

        user_id = decode_token(token).get('user_id')  # Extraire user_id du token
        if user_id is None:
            raise PermissionError("Invalid token: User ID not found.")

        user_session = session.query(UserSession).filter_by(user_id=user_id).first()
        if not user_session:
            raise PermissionError("Authentication required.")
        return function(*args, **kwargs)
    return wrapper

def admin_required(function):
    """
    Decorator that ensures the connected user is an admin before allowing execution of an action.

    Args:
        function: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        PermissionError: If the connected user is not an admin.

    """
    @authenticated_action
    def wrapper(*args, **kwargs):
        session = Session(engine)
        employee = session.query(Employee).get(kwargs['user_id'])
        if not employee or employee.department != Department.ADMIN:
            raise PermissionError("Access denied: Admin privileges required.")
        return function(*args, **kwargs)
    return wrapper

def permission_required(roles):
    """
    Decorator to check if the authenticated user belongs to certain roles/departments.

    Args:
        roles (list): List of roles/departments that the user must belong to.

    Returns:
        function: Decorated function that checks the user's permissions before executing.
    """
    @authenticated_action
    def decorator(function):
        def wrapper(*args, **kwargs):
            session = Session(engine)
            employee = session.query(Employee).get(kwargs['user_id'])
            if not employee or employee.department not in roles:
                raise PermissionError("Permission denied: User is not authorized.")
            return function(*args, **kwargs)
        return wrapper
    return decorator

def create_session(user_id):
    """
    Create a session for the specified user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The generated JWT (JSON Web Token) for the user session.

    Raises:
        Exception: If an error occurs during the session creation.

    """
    session = Session()
    try:
        user_session = UserSession(user_id=user_id)
        session.add(user_session)
        session.commit()
        return user_session.generate_jwt()  # Générer et retourner le JWT
    except Exception as e:
        session.rollback()  # Rollback en cas d'erreur
        raise e
    finally:
        session.close()  # Fermer la session

def delete_session_by_token(token: str, db_session: Session) -> None:
    """
    Delete a user session based on the provided token.

    Args:
        token (str): The token associated with the user session.
        db_session (Session): The database session object.

    Returns:
        None
    """
    user_session = db_session.query(UserSession).filter_by(token=token).first()
    if user_session:
        db_session.delete(user_session)
        db_session.commit()

def get_current_user_token(db_session: Session, user_id: int) -> str:
    """
    Retrieve the current user's token from the database using the user's ID.

    Args:
        db_session (Session): The database session object.
        user_id (int): The ID of the user.

    Returns:
        str: The token of the current user.

    """
    user_session = db_session.query(UserSession).filter_by(user_id=user_id).order_by(UserSession.created_at.desc()).first()
    if user_session:
        return user_session.token
    return None

