# Fonction pour l'écran de connexion
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

def login_view():
    console = Console()
    console.print(Panel("[bold cyan]Bienvenue chez Epic Events CRM[/bold cyan]", expand=False))

    while True:
        username = Prompt.ask("[bold]Nom d'utilisateur[/bold]")
        password = Prompt.ask("[bold]Mot de passe[/bold]", password=True)
        token, error = verify_credentials(username, password)  # Supposons que cette fonction retourne aussi une erreur potentielle

        if token:
            console.print(Panel("[bold green]Connexion réussie[/bold green]", expand=False))
            return token  # Renvoie le token pour qu'il soit utilisé dans les autres parties de l'application
        else:
            console.print(Panel(f"[bold red]Échec de la connexion: {error}[/bold red]", expand=False))
            # Demander à l'utilisateur s'il veut réessayer ou quitter.
            retry = Prompt.ask("[bold]Voulez-vous réessayer? (oui/non)[/bold]").lower()
            if retry != 'oui':
                break

def verify_credentials(username, password):
    # Mettre en œuvre la logique pour vérifier les identifiants de l'utilisateur
    # et retourner un jeton JWT si les identifiants sont corrects.
    # Cette fonction retournerait également une erreur si la vérification échoue.
    pass

def logout_view():
    # logique pour effectuer une déconnexion.
    pass
