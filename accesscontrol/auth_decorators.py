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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = kwargs.get('token')
        if token is None:
            raise PermissionError("Missing authentication token.")

        user = get_user_from_token(token)
        if not user:
            raise PermissionError("Invalid or expired token.")

        # Modifier les kwargs en place si 'user' n'est pas déjà présent
        if 'user' not in kwargs:
            kwargs['user'] = user

        return f(*args, **kwargs)
    return decorated_function

def role_required(department):
    def decorator(f):
        @authenticated
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = kwargs.get('user')
            if not user or user.department != department:
                console.print(f"Accès non autorisé pour les non-membres du département {department}.", style="bold red")
                return
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Décorateur pour exiger des droits d'administrateur
admin_required = role_required(Department.ADMIN)
sales_required = role_required(Department.SALES)
accounting_required = role_required(Department.ACCOUNTING)
support_required = role_required(Department.SUPPORT)
