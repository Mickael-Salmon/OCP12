# accesscontrol/load_current_user.py
import os
import jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models.employees import Employee

# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupère la clé secrète à partir des variables d'environnement
SECRET_KEY = os.getenv('SECRET_KEY')

# Décode le token JWT pour obtenir l'ID de l'utilisateur
def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Le token est expiré
        return None
    except jwt.InvalidTokenError:
        # Le token est invalide
        return None

# Charge les informations de l'utilisateur à partir de la base de données
def load_current_user(token):
    user_id = decode_jwt(token)
    if user_id is not None:
        session = Session()
        try:
            user = session.query(Employee).get(user_id)
            return user
        finally:
            session.close()  # Assurez-vous de fermer la session
    return None
