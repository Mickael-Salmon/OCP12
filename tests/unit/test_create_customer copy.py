"""
This test module is designed to validate the functionality of the ClientsManager class.
It ensures that only authorized roles can perform certain operations like creating a new client.
"""

import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from managers.clients import ClientsManager
from models.clients import Client
from tests.unit.settings_pytest import login_as_sales, login_as_support

FAKE_TEST_CLIENT = {
    "email": "john.tester@test.test",
    "full_name": "John, Tester",
    "phone": "123454321",
    "company": "testers",
    "sales_contact_id": 1,
}

def test_create_client_from_sales_employee(session: Session):
    """
    This test case checks if sales employees are authorized to create a new client.
    It uses a fake client data set and tries to create a new client in the database.
    After creating, it also verifies if the client data matches the original data.
    """
    manager = ClientsManager(session)

    with login_as_sales():
        created_client = manager.create(**FAKE_TEST_CLIENT)

        assert created_client is not None

        created_client = manager.get(Client.full_name == FAKE_TEST_CLIENT["full_name"])[0]

        assert created_client.email == FAKE_TEST_CLIENT["email"]

def test_create_employee_from_unauthorized(session: Session):
    """
    This test case checks if unauthorized roles (like accounting and support)
    are prevented from creating a new client. It tries to create a new client
    while logged in as accounting and support roles and expects a PermissionError.
    """
    manager = ClientsManager(session)

    with login_as_accounting(), pytest.raises(PermissionError):
        manager.create(**FAKE_TEST_CLIENT)

    with login_as_support(), pytest.raises(PermissionError):
        manager.create(**FAKE_TEST_CLIENT)

    request = sqlalchemy.select(Client).where(
        Client.full_name == FAKE_TEST_CLIENT["full_name"]
    )
    assert session.scalars(request).all() == []
