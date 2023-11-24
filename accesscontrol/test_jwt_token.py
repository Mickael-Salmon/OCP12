import jwt
from sqlalchemy.sql import func
from datetime import datetime, timedelta

# Assure-toi d'utiliser la même clé secrète pour le test
SECRET_KEY = "0c3675d17b501c4fdb32718dd19740d2"

def create_token(user_id: int) -> str:
    """
    Create a JWT token for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The JWT token.
    """
    expiration_time = func.now() + timedelta(hours=1)
    return jwt.encode(
        {"exp": expiration_time, "user_id": user_id},
        SECRET_KEY,
        algorithm="HS256"
    )

def decode_token(token: str) -> dict:
    """
    Decode a JWT token and return the payload as a dictionary.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload as a dictionary.

    Raises:
        ValueError: If the token has expired or is invalid.
    """
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
