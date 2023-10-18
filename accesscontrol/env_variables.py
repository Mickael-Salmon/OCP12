"""
This file is responsible for managing environment variables needed for the application.
It checks for the existence of required environment variables (Database credentials, Secret Key) and raises exceptions if they are not set preventing the application from running in an unstable state.
It also provides a utility function to retrieve the application directory path on the user's disk.
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from local file .env
load_dotenv()

####### TO DO ######
####### Add secret key to .env file #######

# Fetching environment variables for database and secret key
DATABASE_USERNAME = os.environ.get("EPICEVENTS_USER")
DATABASE_PASSWORD = os.environ.get("EPICEVENTS_PW")
SECRET_KEY = os.environ.get("EPICEVENTS_SK")

__ENV_NOT_SET_MESSAGE = "Environment variable not set: {name}"

# Check if environment variables are set and raise exceptions if not
if not DATABASE_USERNAME:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="EPICEVENTS_USER"))

if not DATABASE_PASSWORD:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="EPICEVENTS_PW"))

if not SECRET_KEY:
    raise AttributeError(__ENV_NOT_SET_MESSAGE.format(name="SECRET_KEY"))


def get_epicevents_path() -> Path:
    """
    Returns the path of the EpicEvents directory on the user's disk.
    Creates the directory if it does not exist.
    """
    appdata_path = Path(os.environ.get("appdata"))
    epicevent_path = Path(appdata_path, "epicevents")

    if not epicevent_path.exists():
        os.mkdir(epicevent_path)

    return epicevent_path
