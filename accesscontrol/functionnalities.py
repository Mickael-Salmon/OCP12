"""
This file is central to the authentication process in the application.
It provides functionalities for logging in, signing up, and logging out users.
It validates user credentials, creates JWT tokens for authenticated sessions,
and manages the storing and clearing of these tokens.
"""
from sqlalchemy.orm import Session
import sqlalchemy
from models.employees import Employee, Department
from managers.manager import engine
from accesscontrol.jwt_token import create_token, store_token, clear_token


def login(email: str, password: str) -> Employee:
    """
    Create a JWT containing the user ID and store it on the user's disk.
    The application will later check this stored token to determine whether the user is authenticated.
    Returns the retrieved Employee object if the login was successful, otherwise returns None.
    """
    session = Session(engine)
    request = sqlalchemy.select(Employee).where(Employee.email == email)

    employee = session.scalar(request)

    if not employee:
        return None

    password_is_valid = employee.check_password(password)

    if password_is_valid:
        token = create_token(user_id=employee.id)
        store_token(token)
        return employee
    else:
        clear_token()
        return None


def sign_up(full_name: str, email: str, password: str):
    """
    Create a new user in the database without being logged in, then log in the created user.
    As only accounting employees are allowed to create users, the new user will be assigned to the accounting department.
    """
    with Session(engine) as session:
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=Department.ACCOUNTING,
        )

        new_employee.set_password(password)

        session.add(new_employee)
        session.commit()

    login(email, password)


def logout():
    """
    Clear the JWT stored on the user's disk, effectively logging out the user.
    """
    clear_token()
