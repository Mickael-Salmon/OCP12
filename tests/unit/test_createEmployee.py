import pytest
from models.employees import Employee
from models.employees import Department

#Simple Fixture
@pytest.fixture
def simple_sales_employee() -> Employee:
    """
    Fixture for creating a basic sales employee.
    """
    return Employee(
        full_name="John Sales",
        email="john.sales@epicevents.co",
        department=Department.SALES,
    )

def test_sales_employee_fixture(simple_sales_employee):
    """
    Test to ensure the sales employee fixture works as expected.
    """
    assert simple_sales_employee.department == Department.SALES
