"""
This file defines the EmployeeManager class which serves as the business logic layer for the 'Employee' model.
It extends the base Manager class and includes methods for CRUD operations on the 'Employee' table.
The class includes methods to create, read, update, and delete Employee records, making sure that the right permissions are checked before performing certain operations.
"""

from sqlalchemy.orm import Session
from accesscontrol.sec_sessions import permission_required
from models.employees import Employee, Department
from managers.manager import Manager
import typing

class EmployeeManager(Manager):
    """
    Manage the access to the ``Employee`` table, serving as the business logic layer for CRUD operations.
    Extends the base Manager class and includes additional methods specific to the Employee model.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the EmployeeManager with a database session and the Employee model.

        Args:
            session (Session): The database session to be used.
        """
        super().__init__(session=session, model=Employee)

    def get(self, *args, **kwargs) -> typing.List[Employee]:
        """
        Retrieve one or more employee records that match the given conditions.
        Requires the user to be authenticated.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: A list of Employee objects.
        """
        return super().get(*args, **kwargs)

    def all(self) -> typing.List[Employee]:
        """
        Retrieve all employee records from the database.
        Requires the user to be authenticated.

        Returns:
            A list of Employee objects representing all employee records.
        """
        return super().all()

    @permission_required(roles=[Department.ACCOUNTING])
    def create(self, full_name: str, email: str, password: str, department: Department) -> Employee:
        """
        Create a new employee record.

        Args:
            full_name (str): The full name of the employee.
            email (str): The email address of the employee.
            password (str): The password for the employee's account.
            department (Department): The department the employee belongs to.

        Returns:
            Employee: The newly created employee object.

        Raises:
            PermissionError: If the user does not have 'ACCOUNTING' department privileges.
        """
        new_employee = Employee(
            full_name=full_name,
            email=email,
            department=department,
        )
        new_employee.set_password(password)  # Assumes that this method hashes the password
        return super().create(new_employee)

    @permission_required(roles=[Department.ACCOUNTING])
    def update(self, *args, **kwargs) -> Employee:
        """
        Update one or more employee records that match the given conditions.
        Requires the user to have 'ACCOUNTING' department privileges.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Employee: The updated employee record.

        """
        return super().update(*args, **kwargs)

    @permission_required(roles=[Department.ACCOUNTING])
    def delete(self, *args, **kwargs) -> None:
        """
        Delete one or more employee records that match the given conditions.
        Requires the user to have 'ACCOUNTING' department privileges.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        return super().delete(*args, **kwargs)
