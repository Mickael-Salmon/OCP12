from controllers.authentication_controller import logout_user

def logout_view():
    logout_user()
    print("Vous avez été déconnecté.")
