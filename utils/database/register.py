"""
This script serves as the entry point for the user registration functionality in the application.
It prompts the user for necessary credentials and then creates a new user in the database.
Also, it asks for a database password to authorize this action.
"""

from pwinput import pwinput
from accesscontrol.functionnalities import sign_up
from accesscontrol.env_variables import DATABASE_PASSWORD


if __name__ == "__main__":
    """
    Entry point for the registration functionality.
    Collects all required information to create a new user in the database and logs them in.
    """

    # Ask the user for the database password for authorization.
    password = pwinput(
        "You need the database password to access this method.\npassword : "
    )

    # Check if the entered database password is correct.
    if password != DATABASE_PASSWORD:
        print("Invalid password.")
        exit()

    # Collect information to create a new user.
    full_name = input("full name : ")
    email = input("email : ")
    password = pwinput("password : ")

    # Call the sign_up function to create a new user and log them in.
    sign_up(
        full_name=full_name,
        email=email,
        password=password,
    )
