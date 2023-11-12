from accesscontrol.functionnalities import logout
from accesscontrol.jwt_token import decode_token
from rich.console import Console
from rich.panel import Panel

console = Console()

def logout_view(token):
    if token:
        # Décoder le token pour s'assurer qu'il est valide
        user_id = decode_token(token)
        if user_id:
            # Appeler la fonction logout avec le token pour terminer la session
            logout(token)
            console.print(Panel("[bold green]Vous avez été déconnecté avec succès.[/bold green]", expand=False))
        else:
            console.print(Panel("[bold red]La déconnexion a échoué, token invalide.[/bold red]", expand=False))
    else:
        console.print(Panel("[bold red]Aucune session active trouvée.[/bold red]", expand=False))
