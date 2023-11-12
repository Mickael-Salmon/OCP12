import secrets
# Generate a random secret key for the application
# This key will be stores in a file .env in the root directory of the application
secret_key = secrets.token_hex(16)
print(f"Clé secrète générée : {secret_key}")