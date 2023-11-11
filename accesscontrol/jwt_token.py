import datetime
import jwt
from accesscontrol.env_variables import SECRET_KEY

# Algorithm used for JWT
__JWT_ALGORITHM = "HS256"

# The expiration time for the JWT
__JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)

def create_token(user_id: int) -> str:
    """
    Create a JWT for a given user ID.
    The token is encrypted with the secret key and set to expire after a certain duration.
    """
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + __JWT_EXPIRATION_TIME
    return jwt.encode(
        {"exp": expiration_time, "user_id": user_id},
        SECRET_KEY,
        algorithm=__JWT_ALGORITHM
    )

def decode_token(token: str) -> dict:
    """
    Decode the given JWT and return its payload.
    If the token has expired or is invalid, an exception is raised.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[__JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
