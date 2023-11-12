from sqlalchemy import text

class ReportController:
    def __init__(self, session):
        self.session = session

    def get_event_count_by_client(self):
        return self.session.execute(text("""
            SELECT clients.full_name, COUNT(events.id) as event_count
            FROM events
            JOIN contracts ON events.contract_id = contracts.id
            JOIN clients ON contracts.client_id = clients.id
            GROUP BY clients.full_name
        """)).fetchall()

    def get_contract_count_by_sales(self):
        return self.session.execute(text("""
            SELECT employees.full_name, COUNT(contracts.id) as contract_count
            FROM employees
            JOIN contracts ON employees.id = contracts.account_contact_id
            WHERE employees.department = 'SALES'
            GROUP BY employees.full_name;
    """))

    def get_event_count_by_support(self):
        return self.session.execute(text("""
            SELECT employees.full_name, COUNT(events.id) as event_count
            FROM employees
            JOIN events ON employees.id = events.support_contact_id
            WHERE employees.department = 'SUPPORT'
            GROUP BY employees.full_name;
    """))

    def get_total_revenue(self):
        result = self.session.execute(text("""
            SELECT SUM(contracts.total_amount) as total_revenue
            FROM contracts
            WHERE contracts.is_signed = true;
        """)).scalar() # .scalar() pour obtenir la première colonne de la première ligne du résultat
        return result

