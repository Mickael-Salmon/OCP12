from sqlalchemy.orm import Session
from models.user import UserSession
from managers.manager import engine
from cryptography.fernet import Fernet, InvalidToken
import base64
import os

# Charger la clé depuis .env ou générer une nouvelle si elle n'existe pas
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY or len(SECRET_KEY) != 32:
    SECRET_KEY = Fernet.generate_key().decode()
else:
    # S'assurer que la clé est en base64 url-safe
    SECRET_KEY = base64.urlsafe_b64encode(SECRET_KEY.encode()).decode()

def save_token(employee_id, jwt_token):
    """
    Save the JWT token for the given employee ID.

    Parameters:
    - employee_id (int): The ID of the employee.
    - jwt_token (str): The JWT token to be saved.

    Returns:
    None
    """
    cipher_suite = Fernet(SECRET_KEY)
    encrypted_token = cipher_suite.encrypt(jwt_token.encode())
    session = Session(engine)
    new_user_session = UserSession(employee_id=employee_id, token=encrypted_token)
    session.add(new_user_session)
    session.commit()

def load_token(employee_id):
    """
    Load the JWT token for the given employee ID from the database.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        str or None: The JWT token if found, None otherwise.
    """
    session = Session(engine)
    user_session = session.query(UserSession).filter_by(employee_id=employee_id).first()
    if not user_session:
        return None
    cipher_suite = Fernet(SECRET_KEY)
    try:
        jwt_token = cipher_suite.decrypt(user_session.token).decode()
        return jwt_token
    except InvalidToken:
        print("Le token est invalide ou a expiré.")
        # Ici, tu peux également supprimer la session invalide de la base de données
        session.delete(user_session)
        session.commit()
        return None

def clear_token(employee_id):
    """
    Clears the token associated with the given employee ID.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        None
    """
    session = Session(engine)
    session.query(UserSession).filter_by(employee_id=employee_id).delete()
    session.commit()
