"""
This script serves as the entry point for the logout feature of the application. It deletes the authentication token stored on the user's disk, effectively logging out the user.
"""

from accesscontrol.functionnalities import logout


if __name__ == "__main__":
    """
    Entry point for the Logout feature. Deletes the token stored on the user's disk.
    """

    # Perform logout by deleting the stored token.
    logout()
