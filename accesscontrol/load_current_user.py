# accesscontrol/load_current_user.py
from sqlalchemy.orm import Session
from models.employees import Employee
from accesscontrol.jwt_token import decode_token  # Assuming this function exists and is properly secured

def load_current_user(token):
    """
    Load the current user based on the provided JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        Employee: The employee object if the token is valid and the user exists, None otherwise.
    """
    user_id = decode_token(token)  # Use the secure decode function from jwt_token.py
    if user_id is None:
        return None

    with Session() as session:
        try:
            user = session.query(Employee).get(user_id)
            return user
        except Exception as e:
            # Handle the exception as necessary
            return None
