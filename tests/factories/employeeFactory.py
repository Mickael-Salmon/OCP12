from models.employees import Employee, Department
from datetime import datetime
from faker import Faker

fake = Faker()

class EmployeeFactory:
    def __init__(self, department=Department.ACCOUNTING):
        self.full_name = fake.name()
        self.email = f"{fake.email().split('@')[0]}+{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        self.department = department

    def create(self):
        employee = Employee(
            full_name=self.full_name,
            email=self.email,
            department=self.department
        )
        employee.set_password('PasswordTest123')  # On peut aussi passer un mot de passe généré aléatoirement ici
        return employee
