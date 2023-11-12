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
    return Session(engine)

# Créer un token JWT pour un utilisateur donné
def create_jwt_token(user_id):
    with get_db_session() as session:
        user_session = UserSession(user_id=user_id)
        session.add(user_session)
        session.commit()
        return create_token(user_id)

# Vérifier le token JWT et récupérer l'utilisateur
def get_user_from_token(token):
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

        return f(*args, user=user, **kwargs)
    return decorated_function

# Décorateur pour exiger des droits d'administrateur
def admin_required(f):
    @authenticated
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = kwargs.get('user')
        if not user or user.department != Department.ADMIN:
            console.print("Accès non autorisé ! Merci de contacter l'administrateur.", style="bold red")
            return  # Ici, on arrête l'exécution et on retourne au menu principal
        return f(*args, **kwargs)
    return decorated_function
