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

