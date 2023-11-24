import pytest
from sqlalchemy import create_engine
from accesscontrol.sec_sessions import Session, UserSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models.employees import Department
from tests.factories.employeeFactory import EmployeeFactory
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configurer la connexion à la base de données de test
DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def simple_sales_employee():
    return EmployeeFactory(department=Department.SALES).create()


def test_sales_employee_fixture(simple_sales_employee):
    assert simple_sales_employee.department == Department.SALES


@pytest.fixture
def sales_employee():
    return EmployeeFactory(department=Department.SALES).create()

@pytest.fixture
def accounting_employee():
    return EmployeeFactory(department=Department.ACCOUNTING).create()


def test_filter_employee_by_department(sales_employee, accounting_employee):
    all_employees = [sales_employee, accounting_employee]
    sales_employees = [e for e in all_employees if e.department == Department.SALES]

    assert len(sales_employees) == 1
    assert sales_employees[0].department == Department.SALES