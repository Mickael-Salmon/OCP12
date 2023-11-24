from functools import wraps
from sqlalchemy.orm import Session
from models.user import UserSession
from accesscontrol.jwt_token import decode_token, create_token
from managers.manager import engine
from models.employees import Department, Employee
from rich.console import Console
console = Console()

# Utilitaire pour créer une session de base de données
def get_db_session():
    """
    Returns a database session object.
    """
    return Session(engine)

# Créer un token JWT pour un utilisateur donné
def create_jwt_token(user_id):
    """
    Creates a JWT token for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The JWT token.
    """
    with get_db_session() as session:
        user_session = UserSession(user_id=user_id)
        session.add(user_session)
        session.commit()
        return create_token(user_id)

# Vérifier le token JWT et récupérer l'utilisateur
def get_user_from_token(token):
    """
    Retrieves the user associated with the given token.

    Args:
        token (str): The token to decode and retrieve the user from.

    Returns:
        Employee: The employee object corresponding to the user.

    """
    user_id = decode_token(token).get('user_id')
    with get_db_session() as session:
        return session.query(Employee).get(user_id)

# Décorateur pour authentifier les utilisateurs
def authenticated(f):
    """
    Decorator function to authenticate user before executing the decorated function.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        PermissionError: If the authentication token is missing, invalid, or expired.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = kwargs.get('token')
        if token is None:
            raise PermissionError("Missing authentication token.")

        user = get_user_from_token(token)
        if not user:
            raise PermissionError("Invalid or expired token.")

        return f(*args, user=user, **kwargs)
    return decorated_function

# Décorateur pour exiger des droits d'administrateur
def admin_required(f):
    """
    Decorator that checks if the user is an admin before executing the decorated function.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        None

    """
    @authenticated
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = kwargs.get('user')
        if not user or user.department != Department.ADMIN:
            console.print("Accès non autorisé ! Merci de contacter l'administrateur.", style="bold red")
            return  # Ici, on arrête l'exécution et on retourne au menu principal
        return f(*args, **kwargs)
    return decorated_function
