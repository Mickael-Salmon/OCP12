from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

# Initialize the Console object from Rich
console = Console()

# Create a table
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Test Description", style="dim", width=50)
table.add_column("Status")

# Load Environment variables
load_dotenv()

# Get the database url from environment variables
database_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(database_url, echo=True)

# Connection test
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        if result.fetchone()[0] == 1:
            table.add_row("Database Connection", "[green]Passed[/green]")
            console.print(Panel.fit("[green]All Tests Passed Successfully[/green]", title="DB Connection Test Summary"))
        else:
            table.add_row("Database Connection", "[red]Failed[/red]")
            console.print(Panel.fit("[red]Some Tests Failed[/red]", title="DB Connection Test Summary"))
except Exception as e:
    table.add_row("Database Connection", f"[red]Error: {e}[/red]")
    console.print(Panel.fit("[red]Some Tests Failed[/red]", title="DB Connection Test Summary"))

# Print the table
console.print(table)
