from sqlalchemy import inspect
from rich.console import Console
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load Environment variables
load_dotenv()

# Get the database url from environment variables
database_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(database_url, echo=True)
# Initialize the Console object from Rich
console = Console()

# Create the database engine (assuming 'engine' has already been created)
# engine = create_engine(database_url, echo=True)

# Initialize inspector and get table names
inspector = inspect(engine)
table_names = inspector.get_table_names()

# Rich Display
console.print("[yellow]List of tables in the database:[/yellow]")
for table in table_names:
    console.print(f"[green]✔ {table}[/green]")
