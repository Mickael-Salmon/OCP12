from sqlalchemy.orm import Session
import sqlalchemy
from models.employees import Employee, Department
from managers.manager import engine
from accesscontrol.jwt_token import create_token
from models.user import UserSession
from typing import Tuple, Optional
import bcrypt

def login(email: str, password: str) -> Employee:
    """
    Validate user credentials, create a JWT token, store it in the user_sessions table,
    and return the Employee object if the login was successful.
    """
    with Session(engine) as session:
        employee = session.query(Employee).filter(Employee.email == email).first()

        if employee and bcrypt.checkpw(password.encode('utf-8'), employee.password_hash.encode('utf-8')):
            token = create_token(user_id=employee.id)
            user_session = UserSession(user_id=employee.id)
            session.add(user_session)
            session.commit()
            return employee, user_session.token
    return None, None  # Always return a tuple to match expected return type


def logout(token: str):
    """
    Clear the JWT from the user_sessions table, effectively logging out the user.
    """
    with Session(engine) as session:
        user_session = session.query(UserSession).filter_by(token=token).first()
        if user_session:
            session.delete(user_session)
            session.commit()
