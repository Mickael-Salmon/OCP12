from accesscontrol.functionnalities import login

def login_view():
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")

    user_id, token = login(username, password)

    if user_id:
        print("Connexion réussie.")
        return user_id, token
    else:
        print("Identifiants incorrects.")
        return None, None


