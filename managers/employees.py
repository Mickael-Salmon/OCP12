"""
This file defines the EmployeeManager class which serves as the business logic layer for the 'Employee' model.
It extends the base Manager class and includes methods for CRUD operations on the 'Employee' table.
The class includes methods to create, read, update, and delete Employee records, making sure that the right permissions are checked before performing certain operations.
"""
import typing
from sqlalchemy.orm import Session

from authentification.decorators import login_required, permission_required
from models.employees import Employee, Department
from database.manager import Manager, engine


class EmployeeManager(Manager):
    """
    Manage the access to the ``Employee`` table, serving as the business logic layer for CRUD operations.
    Extends the base Manager class and includes additional methods specific to the Employee model.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the EmployeeManager with a database session and the Employee model.
        """
        super().__init__(session=session, model=Employee)

    @login_required
    def get(self, *args, **kwargs) -> typing.List[Employee]:
        """
        Retrieve one or more employee records that match the given conditions.
        Requires the user to be logged in.
        """
        return super().get(*args, **kwargs)

    @login_required
    def all(self) -> typing.List[Employee]:
        """
        Retrieve all employee records from the database.
        Requires the user to be logged in.
        """
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING])
    def create(self, full_name: str, email: str, password: str, department: Department):
        """
        Create a new employee record.
        Requires the user to have 'ACCOUNTING' department privileges.
        Hashes the password before storing it.
        """
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )
        new_employee.set_password(password)
        return super().create(new_employee)

    @permission_required(roles=[Department.ACCOUNTING])
    def update(self, *args, **kwargs):
        """
        Update one or more employee records that match the given conditions.
        Requires the user to have 'ACCOUNTING' department privileges.
        """
        return super().update(*args, **kwargs)

    @permission_required(roles=[Department.ACCOUNTING])
    def delete(*args, **kwargs):
        """
        Delete one or more employee records that match the given conditions.
        Requires the user to have 'ACCOUNTING' department privileges.
        """
        return super().delete(**kwargs)
