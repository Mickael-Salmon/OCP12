from sqlalchemy import text

class ReportController:
    """
    Controller class for generating reports.
    """

    def __init__(self, session):
        """
        Initializes a new instance of the ReportController class.

        Args:
            session: The database session to use for executing queries.
        """
        self.session = session

    def get_event_count_by_client(self):
        """
        Retrieves the event count grouped by client.

        Returns:
            A list of tuples containing the client's full name and the event count.
        """
        return self.session.execute(text("""
            SELECT clients.full_name, COUNT(events.id) as event_count
            FROM events
            JOIN contracts ON events.contract_id = contracts.id
            JOIN clients ON contracts.client_id = clients.id
            GROUP BY clients.full_name
        """)).fetchall()

    def get_contract_count_by_sales(self):
        """
        Retrieves the contract count grouped by sales employees.

        Returns:
            A list of tuples containing the sales employee's full name and the contract count.
        """
        return self.session.execute(text("""
            SELECT employees.full_name, COUNT(contracts.id) as contract_count
            FROM employees
            JOIN contracts ON employees.id = contracts.account_contact_id
            WHERE employees.department = 'SALES'
            GROUP BY employees.full_name;
    """))

    def get_event_count_by_support(self):
        """
        Retrieves the event count grouped by support employees.

        Returns:
            A list of tuples containing the support employee's full name and the event count.
        """
        return self.session.execute(text("""
            SELECT employees.full_name, COUNT(events.id) as event_count
            FROM employees
            JOIN events ON employees.id = events.support_contact_id
            WHERE employees.department = 'SUPPORT'
            GROUP BY employees.full_name;
    """))

    def get_total_revenue(self):
        """
        Retrieves the total revenue from signed contracts.

        Returns:
            The total revenue as a decimal value.
        """
        result = self.session.execute(text("""
            SELECT SUM(contracts.total_amount) as total_revenue
            FROM contracts
            WHERE contracts.is_signed = true;
        """)).scalar() # .scalar() to get the first column of the first row of the result
        return result

