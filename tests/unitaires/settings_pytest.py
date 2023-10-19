"""
This conftest.py file is responsible for setting up the test environment.
It defines pytest fixtures for reusable components and also configures the test database.
"""

import pytest
from contextlib import contextmanager
from sqlalchemy.orm import Session
import sqlalchemy
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Create a PostgreSQL test engine
__TEST_ENGINE = sqlalchemy.create_engine(
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/epicevents_test"
)


# -----------------------------------
# Database test data fixtures
# -----------------------------------
@pytest.fixture
def sales_employee() -> Employee:
    """
    Fixture for creating a sales employee.
    """
    employee = Employee(
        full_name="sales, employee",
        email="sales.employee@epicevents.co",
        department=Department.SALES,
    )
    employee.set_password("password")
    return employee


@pytest.fixture
def account_employee() -> Employee:
    """
    Fixture for creating an accounting employee.
    """
    # ... (Same as your existing code)


# -----------------------------------
# Database setup fixtures
# -----------------------------------
@pytest.fixture(scope="function")
def setup_database():
    """
    Fixture for setting up and tearing down the test database.
    """
    Base.metadata.create_all(__TEST_ENGINE)
    yield
    Base.metadata.drop_all(__TEST_ENGINE)


# -----------------------------------
# Session fixture
# -----------------------------------
@pytest.fixture(scope="function")
def session(setup_database, account_employee, sales_employee, support_employee, client, contract, event):
    """
    Fixture for setting up a session for database operations.
    """
    # ... (Same as your existing code)


# -----------------------------------
# Login context managers
# -----------------------------------
@contextmanager
def login_as_sales():
    """
    Context manager for simulating login as a sales employee.
    """
    try:
        token = create_token(user_id=1)
        store_token(token)
        yield
    finally:
        clear_token()

@contextmanager
def login_as_support():
    try:
        token = create_token(user_id=3)
        store_token(token)
        yield
    finally:
        clear_token()
