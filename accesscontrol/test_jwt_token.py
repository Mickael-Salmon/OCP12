import jwt
from datetime import datetime, timedelta

# Assure-toi d'utiliser la même clé secrète pour le test
SECRET_KEY = "0c3675d17b501c4fdb32718dd19740d2"

def create_token(user_id: int) -> str:
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(
        {"exp": expiration_time, "user_id": user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

# Test
user_id = 123
token = create_token(user_id)
print("Token:", token)

try:
    decoded = decode_token(token)
    print("Decoded:", decoded)
except ValueError as e:
    print("Error decoding token:", e)
