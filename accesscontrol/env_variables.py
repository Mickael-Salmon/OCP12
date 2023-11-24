from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from local file .env
load_dotenv()

# Fetching environment variables for database and secret key
DATABASE_USERNAME = os.environ.get("EPICEVENTS_USER")
DATABASE_PASSWORD = os.environ.get("EPICEVENTS_PW")
SECRET_KEY = os.environ.get("SECRET_KEY")

__ENV_NOT_SET_MESSAGE = "Environment variable not set: {}"

# Check if environment variables are set and raise exceptions if not
if not DATABASE_USERNAME:
    raise EnvironmentError(__ENV_NOT_SET_MESSAGE.format("EPICEVENTS_USER"))

if not DATABASE_PASSWORD:
    raise EnvironmentError(__ENV_NOT_SET_MESSAGE.format("EPICEVENTS_PW"))

if not SECRET_KEY:
    raise EnvironmentError(__ENV_NOT_SET_MESSAGE.format("SECRET_KEY"))

def get_database_username() -> str:
    """
    Get the value of the EPICEVENTS_USER environment variable.

    Returns:
        str: The value of the EPICEVENTS_USER environment variable.
    """
    return DATABASE_USERNAME

def get_database_password() -> str:
    """
    Get the value of the EPICEVENTS_PW environment variable.

    Returns:
        str: The value of the EPICEVENTS_PW environment variable.
    """
    return DATABASE_PASSWORD

def get_secret_key() -> str:
    """
    Get the value of the SECRET_KEY environment variable.

    Returns:
        str: The value of the SECRET_KEY environment variable.
    """
    return SECRET_KEY
