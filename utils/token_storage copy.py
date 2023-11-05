from cryptography.fernet import Fernet, InvalidToken
import os
import base64

# Charger la clé depuis .env ou générer une nouvelle si elle n'existe pas
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY or len(SECRET_KEY) != 32:
    SECRET_KEY = Fernet.generate_key().decode()
else:
    # S'assurer que la clé est en base64 url-safe
    SECRET_KEY = base64.urlsafe_b64encode(SECRET_KEY.encode()).decode()

def save_token(jwt_token):
    cipher_suite = Fernet(SECRET_KEY)
    encrypted_token = cipher_suite.encrypt(jwt_token.encode())
    with open('session/token.txt', 'wb') as file:
        file.write(encrypted_token)


def load_token():
    cipher_suite = Fernet(SECRET_KEY)
    with open('session/token.txt', 'rb') as file:
        encrypted_token = file.read()
    try:
        jwt_token = cipher_suite.decrypt(encrypted_token).decode()
        return jwt_token
    except InvalidToken:
        print("Le token est invalide ou a expiré.")
        return None


def clear_token():
    if os.path.exists('session/token.txt'):
        os.remove('session/token.txt')

def delete_token():
    # Supprime le fichier token.txt s'il existe
    if os.path.exists('session/token.txt'):
        os.remove('session/token.txt')

