﻿from accesscontrol.functionnalities import login
import pwinput
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def login_view():
    """
    Displays a login view for the Epic Events CRM.

    Returns:
        tuple: A tuple containing the user ID and token if the login is successful, otherwise None.
    """
    console.print(Markdown("# 🚀 Connexion à Epic Events CRM"), style="bold magenta")

    username = Prompt.ask("👤 Nom d'utilisateur")
    password = pwinput.pwinput(prompt="🔑 Mot de passe: ")
    user_id, token, user_name = login(username, password)

    if user_id:
        console.print(Panel(f"[bold green]Connexion réussie! Bienvenue, {user_name}[/bold green]", expand=False))
        return user_id, token, user_name
    else:
        console.print(Panel("[bold red]Identifiants incorrects.[/bold red]", expand=False))
        return None, None, None
