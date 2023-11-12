from sqlalchemy import create_engine
from dotenv import load_dotenv
from rich.console import Console
import os

# Initialize Rich console
console = Console()

# Load the environment variables
load_dotenv()

# Get the database URL from the environment variable
database_url = os.getenv("DATABASE_URL")

# Check if the database URL is available
if database_url is None:
    console.print("[red]Error: DATABASE_URL not found in environment variables.[/red]")
    exit()

# Create the database engine
try:
    engine = create_engine(database_url)
    console.print(f"[green]Successfully connected to database at {database_url}[/green]")
except Exception as e:
    console.print(f"[red]Error while connecting to database: {e}[/red]")
    exit()

# Assuming that your Base class is in a module called 'models'
try:
    from models import Base  # Import the Base object from your models module
    # Create all tables in the database which are defined by the classes that extend the Base class
    Base.metadata.create_all(engine)
    console.print("[green]Successfully created tables in the database.[/green]")
except Exception as e:
    console.print(f"[red]Error while creating tables: {e}[/red]")
