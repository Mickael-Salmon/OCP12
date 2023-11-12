import pytest
from models.employees import Department
from factories.employeeFactory import EmployeeFactory

@pytest.fixture
def simple_sales_employee():
    return EmployeeFactory()

def test_sales_employee_fixture(simple_sales_employee):
    assert simple_sales_employee.department == Department.SALES


@pytest.fixture
def sales_employee():
    return EmployeeFactory()

@pytest.fixture
def accounting_employee():
    return EmployeeFactory(department=Department.ACCOUNTING)

def test_filter_employee_by_department(sales_employee, accounting_employee):
    all_employees = [sales_employee, accounting_employee]
    sales_employees = [e for e in all_employees if e.department == Department.SALES]

    assert len(sales_employees) == 1
    assert sales_employees[0].department == Department.SALES
