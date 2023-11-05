"""
This file serves as the core component for managing JSON Web Tokens (JWT) within the application.
It contains functions that allow for the creation, storage, retrieval, and validation of JWTs.
The tokens are used to securely manage user sessions and to ensure that users are authenticated
before accessing certain parts of the application.
"""
from pathlib import Path
import datetime
import os
import jwt
from accesscontrol.env_variables import get_epicevents_path, SECRET_KEY

# Algorithm used for JWT
__JWT_ALGORITHM = "HS256"

# The expiration time for the JWT
__JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)

# File comment explaining the role of this file in the application
"""
This file is responsible for managing JSON Web Tokens (JWT) for user authentication.
It provides functions to store, retrieve, create, and decode JWT, as well as to get the authenticated user's ID.
This ensures that only authorized users can access certain parts of the application.
"""

def __get_token_path() -> Path:
    """
    Retrieve the path where the token is stored.
    """
    return Path(get_epicevents_path(), "token.txt")

def store_token(token: str):
    """
    Store the given JWT to the user's disk.
    """
    path = __get_token_path()
    with open(path, "w") as writer:
        writer.write(token)

def retreive_token() -> str:
    """
    Retrieve the stored JWT from the user's disk.
    Returns None if no token is found.
    """
    path = __get_token_path()
    if not path.exists():
        return None
    with open(path, "r") as reader:
        return reader.read()

def clear_token():
    """
    Remove the JWT stored on the user's disk.
    """
    path = __get_token_path()
    if path.exists():
        os.remove(path)

def create_token(user_id: int) -> str:
    """
    Create a JWT for a given user ID.
    The token is encrypted with a secret key and set to expire after a certain duration.
    """
    expiration_time = datetime.datetime.utcnow() + __JWT_EXPIRATION_TIME
    return jwt.encode(
        payload={"exp": expiration_time, "user_id": user_id},
        key=SECRET_KEY,
        algorithm=__JWT_ALGORITHM,
    )

def decode_token(token: str) -> dict:
    """
    Decode the given JWT and return its payload.
    If the token has expired or is invalid, it is cleared from the disk and None is returned.
    """
    try:
        return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=__JWT_ALGORITHM)
    except Exception:
        # Token is expired or is not valid
        clear_token()
        return None

def get_authenticated_user_id() -> int:
    """
    Retrieve the ID of the authenticated user from the stored token.
    """
    stored_token = retreive_token()
    if not stored_token:
        return None
    token_payload = decode_token(stored_token)
    return token_payload["user_id"]
