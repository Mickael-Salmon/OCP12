"""
This file contains decorators used to address security mechanisms within the application like authorization and authentication.
It ensures that only authenticated users can access certain parts of the application and that they have the appropriate permissions.
It contains decorators that are used to protect routes and functions, ensuring that only authorized and authenticated users can perform certain actions.
It does maintain the integrity and confidentiality of the application data.
"""

from sqlalchemy.orm import Session
import sqlalchemy
import typing

from authentification.token import decode_token, retreive_token
from models.employees import Employee, Department
from database.manager import engine

def login_required(function):
    """
    Decorator for checking if the current user is authenticated.
    It tries to retrieve and decode the token stored on the user's disk.

    Raises:
    * PermissionError: If authentication fails.
    """
    def wrapper(*args, **kwargs):
        token = retreive_token()

        if not decode_token(token):
            raise PermissionError("Please login and retry.")

        return function(*args, **kwargs)

    return wrapper

def permission_required(roles: typing.List[Department]):
    """
    Decorator for checking if the authenticated user belongs to a certain department.

    Args:
    * roles (List[Department]): A list of Department enums that are authorized to access the function.

    Raises:
    * PermissionError: If the user does not have permission to access the function.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            REJECT_MESSAGE = "Permission denied."

            token = retreive_token()
            token_payload = decode_token(token)

            if not token_payload:
                raise PermissionError(REJECT_MESSAGE)

            user_id = token_payload["user_id"]

            session = Session(engine)
            request = sqlalchemy.select(Employee).where(Employee.id == user_id)
            employee = session.scalar(request)

            if not employee:
                raise PermissionError(REJECT_MESSAGE)

            if employee.department not in roles:
                raise PermissionError(REJECT_MESSAGE)

            return function(*args, **kwargs)

        return wrapper

    return decorator
