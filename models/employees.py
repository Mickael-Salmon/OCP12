"""
This file defines the Employee model, which represents an employee entity in the application.
The model includes various fields like full_name, email, password_hash, and salt, among others.
It also includes methods for password hashing and verification.
The model specifies the 'department' field as an Enum, representing the department to which the employee belongs.
"""
from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum  # Importing column types
from sqlalchemy.orm import relationship  # To define the relationship
import enum  # Python's standard library for enum types
import bcrypt  # Library for hashing passwords
from datetime import datetime

class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    token = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    employee = relationship("Employee", back_populates="sessions")  # Link to the Employee model

class Department(enum.Enum):  # Enum class to represent different departments
    """
    Enum to define possible department values for employees.
    """
    ADMIN = "admin"
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
    # Add a new relationship to link with the UserSession model
    sessions = relationship("UserSession", back_populates="employee", cascade="all, delete-orphan")

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
