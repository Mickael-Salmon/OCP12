"""
This script serves as the entry point for the login feature of the application.
It takes the email and password as command-line arguments or user input and then attempts to log in the user.
If successful, it prints a welcome message; otherwise, it prints an "Invalid credentials" message.
"""

import sys
from pwinput import pwinput
from accesscontrol.functionnalities import login


if __name__ == "__main__":
    """
    Entry point for the login feature. It accepts email and password either from command-line arguments or user input.
    """

    args = sys.argv
    # Get email from command-line arguments, if provided.
    email = args[1] if len(args) > 1 else input("email: ")
    # Securely get password input.
    password = pwinput("password: ")

    # Attempt to log in.
    logged_in_employee = login(email, password)

    # Check if login was successful.
    if not logged_in_employee:
        print("Invalid credentials")
    else:
        print(f"Welcome {logged_in_employee.full_name}!")
