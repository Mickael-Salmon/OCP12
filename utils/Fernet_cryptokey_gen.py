from cryptography.fernet import Fernet

def generate_fernet_key():
    """
    Generates a Fernet key and prints it for copying.
    """
    key = Fernet.generate_key()
    print(key.decode('utf-8'))

generate_fernet_key()
