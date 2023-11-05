from cryptography.fernet import Fernet

# Génère une clé Fernet
key = Fernet.generate_key()

# Affiche la clé pour que tu puisses la copier
print(key.decode('utf-8'))
