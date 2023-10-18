﻿from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import Enum, Column, Integer, String, DateTime  # Importing column types
import enum  # Python's standard library for enum types
import bcrypt  # Library for hashing passwords

class Department(enum.Enum):  # Enum class to represent different departments
    """
    Enum to define possible department values for employees.
    """
    SALES = "sales"
    ACCOUNTING = "accounting"
    SUPPORT = "support"


class Employee(Base):  # Employee model class inheriting from Base
    """
    This is the Employee model class. It defines the attributes and behaviors associated with
    an employee in the application.
    """

    __tablename__ = "employees"  # Specifying the table name in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    """
    The unique identifier for an employee.
    """

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    """
    The date and time when the employee record was created.
    """

    full_name = Column(String(50), nullable=False)
    """
    The full name of the employee.
    """

    email = Column(String(50), nullable=False, unique=True)
    """
    The email address of the employee. Must be unique.
    """

    password_hash = Column(String(60), nullable=False)
    """
    The hashed password of the employee.
    """

    salt = Column(String(30), nullable=False)
    """
    The salt value used in password hashing.
    """

    department = Column(Enum(Department), nullable=False)
    """
    The department the employee belongs to. Values are constrained by the 'Department' enum.
    """

    def set_password(self, password: str):
        """
        Hash and store a new password + salt value.
        Generates a new salt and hashes the provided password using bcrypt.
        """
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)
        self.password_hash = password_hash.decode("utf-8")
        self.salt = salt.decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        Check if a given password is valid, regarding the registered hashed password.
        Uses bcrypt to compare the provided password against the stored hashed password.
        """
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=self.password_hash.encode("utf-8"),
        )
