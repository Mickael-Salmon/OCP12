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
    def wrapper(*args, **kwargs):
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
    """
    user_session = db_session.query(UserSession).filter_by(token=token).first()
    if user_session:
        db_session.delete(user_session)
        db_session.commit()

def get_current_user_token(db_session: Session, user_id: int) -> str:
    """
    Retrieve the current user's token from the database using the user's ID.
    """
    user_session = db_session.query(UserSession).filter_by(user_id=user_id).order_by(UserSession.created_at.desc()).first()
    if user_session:
        return user_session.token
    return None

