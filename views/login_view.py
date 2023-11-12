from accesscontrol.functionnalities import login
import pwinput
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def login_view():
    console.print(Markdown("# 🚀 Connexion à Epic Events CRM"), style="bold magenta")

    username = Prompt.ask("👤 Nom d'utilisateur")
    password = pwinput.pwinput(prompt="🔑 Mot de passe: ")  # masque la saisie du mot de passe

    user_id, token = login(username, password)

    if user_id:
        console.print(Panel("[bold green]Connexion réussie![/bold green]", expand=False))
        return user_id, token
    else:
        console.print(Panel("[bold red]Identifiants incorrects.[/bold red]", expand=False))
        return None, None
