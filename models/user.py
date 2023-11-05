import bcrypt
import jwt
import os
import psycopg2
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()
sentry_sdk.init(dsn=os.getenv('SENTRY_DSN'), environment="development")

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

def verify_credentials(username, password):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM employees WHERE email = %s", (username,))
        user_record = cursor.fetchone()

        if user_record:
            password_hash = user_record[0]

            # Convertit le hash en bytes si ce n'est pas déjà le cas
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')

            # Convertit le mot de passe en bytes pour la vérification
            password_bytes = password.encode('utf-8')

            if bcrypt.checkpw(password_bytes, password_hash):
                # Les identifiants sont corrects, générer le token JWT
                token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
                return token
        return None
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
    finally:
        cursor.close()
        conn.close()


