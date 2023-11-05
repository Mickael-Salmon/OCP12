"""
This file contains decorators used to address security mechanisms within the application like authorization and authentication.
It ensures that only authenticated users can access certain parts of the application and that they have the appropriate permissions.
It contains decorators that are used to protect routes and functions, ensuring that only authorized and authenticated users can perform certain actions.
It does maintain the integrity and confidentiality of the application data.
"""

from sqlalchemy.orm import Session
import sqlalchemy
import typing
from accesscontrol.jwt_token import decode_token, retreive_token
from models.employees import Employee, Department
from managers.manager import engine

def authenticated_action(function):
    """
    Decorateur qui vérifie la présence d'un token avant de permettre l'exécution d'une action nécessitant une authentification.
    """
    def wrapper(*args, **kwargs):
        token = retreive_token()
        if not decode_token(token):
            # Logique pour gérer l'échec d'authentification...
            return
        return function(*args, **kwargs)
    return wrapper

def admin_required(function):
    """
    Decorateur qui vérifie que l'utilisateur connecté est un administrateur avant de permettre l'exécution d'une action.
    """
    @authenticated_action
    def wrapper(*args, **kwargs):
        token = retreive_token()
        token_payload = decode_token(token)
        user_id = token_payload["user_id"]

        session = Session(engine)  # Assure-toi que Session et engine sont importés correctement
        employee = session.query(Employee).get(user_id)

        if not employee or employee.department != Department.ADMIN:
            raise PermissionError("Accès refusé : Vous devez être connecté en tant qu'administrateur.")

        return function(*args, **kwargs)
    return wrapper


def permission_required(roles: typing.List[Department]):
    """
    Decorateur pour vérifier si l'utilisateur authentifié appartient à un certain département.
    """
    @authenticated_action
    def decorator(function):
        def wrapper(*args, **kwargs):
            token = retreive_token()
            token_payload = decode_token(token)
            user_id = token_payload["user_id"]

            session = Session(engine)  # Assure-toi que Session et engine sont importés correctement
            employee = session.query(Employee).get(user_id)

            if not employee or employee.department not in roles:
                raise PermissionError("Permission refusée : Utilisateur non autorisé.")

            return function(*args, **kwargs)
        return wrapper
    return decorator

