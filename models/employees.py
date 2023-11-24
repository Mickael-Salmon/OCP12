"""
This file defines the Employee model, which represents an employee entity in the application.
The model includes various fields like full_name, email, and password_hash, among others.
It also includes methods for password hashing and verification.
The model specifies the 'department' field as an Enum, representing the department to which the employee belongs.
"""
from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum  # Importing column types
from sqlalchemy.orm import relationship, validates  # To define the relationship and validation
import enum  # Python's standard library for enum types
import bcrypt  # Library for hashing passwords
import re  # Regular expression library for validation patterns

# Enum class to represent different departments
class Department(enum.Enum):
    ADMIN = "admin"
    SALES = "sales"
    ACCOUNTING = "accounting"
    SUPPORT = "support"

# Employee model class inheriting from Base
class Employee(Base):
    """
    Represents an employee in the system.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    full_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(60), nullable=False)
    department = Column(Enum(Department), nullable=False)
    # Relationship to link with the UserSession model
    sessions = relationship("UserSession", back_populates="employee", cascade="all, delete-orphan")

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(f"Invalid email address: {email}")
        return email

    def set_password(self, password: str):
        """
        Sets the password for the employee.

        Args:
            password (str): The password to set.

        Raises:
            ValueError: If the password is less than 8 characters long.
        """
        if len(password) < 8:  # Example condition, you might want to make this more complex
            raise ValueError("Password must be at least 8 characters long")
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the employee's password.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


