import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.employees import Employee

class TestEmployee(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Employee.metadata.create_all(engine)

    def tearDown(self):
        # Clean up the database after each test
        self.session.rollback()
        Employee.metadata.drop_all(self.session.bind)

    def test_set_password(self):
        employee = Employee(full_name="John Doe", email="john@example.com", department="IT")
        employee.set_password("password123")
        self.assertTrue(employee.check_password("password123"))

    def test_check_password(self):
        employee = Employee(full_name="John Doe", email="john@example.com", department="IT")
        employee.set_password("password123")
        self.assertTrue(employee.check_password("password123"))
        self.assertFalse(employee.check_password("wrongpassword"))

    def test_validate_email(self):
        employee = Employee(full_name="John Doe", email="john@example.com", department="IT")
        self.assertEqual(employee.email, "john@example.com")
        with self.assertRaises(ValueError):
            employee.email = "invalidemail"

if __name__ == '__main__':
    unittest.main()