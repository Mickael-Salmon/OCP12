import pytest
from models import employees


class TestCodeUnderTest:
    """
    A test class that contains multiple test methods to test the functionality of the `set_password` method in the `Employee` class.
    """

    # Test setting a valid password
    def test_set_valid_password(self):
        """
        Test case to verify that a valid password can be set successfully.
        """
        employee = employees()
        employee.set_password("password")
        assert employee.password_hash is not None

    # Test setting an empty password
    def test_set_empty_password(self):
        """
        Test case to verify that an empty password cannot be set.
        """
        employee = employees()
        employee.set_password("")
        assert employee.password_hash is None

    # Test setting a password with special characters
    def test_set_password_special_characters(self):
        """
        Test case to verify that a password with special characters can be set successfully.
        """
        employee = employees()
        employee.set_password("!@#$%^&*")
        assert employee.password_hash is not None

    # Test setting a password with length 0
    def test_set_password_length_0(self):
        """
        Test case to verify that a password with length 0 cannot be set.
        """
        employee = employees()
        employee.set_password("")
        assert employee.password_hash is None

    # Test setting a password with length 1
    def test_set_password_length_1(self):
        """
        Test case to verify that a password with length 1 can be set successfully.
        """
        employee = employees()
        employee.set_password("a")
        assert employee.password_hash is not None

    # Test setting a password with length 255
    def test_set_password_length_255(self):
        """
        Test case to verify that a password with length 255 can be set successfully.
        """
        employee = employees()
        password = "a" * 255
        employee.set_password(password)
        assert employee.password_hash is not None
