# main.py
from views.menu import main as menu_main
from managers.manager import create_tables
import sentry_sdk

sentry_sdk.init(
    dsn="https://1cb6736896ca8c1a4ee88a9a572e8ef6@o4506162192318464.ingest.sentry.io/4506162210013184",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

def main():
    """
    This is the main function of the program.
    It initializes the Sentry SDK, creates tables, and starts the main menu.
    """
    create_tables()
    menu_main()

if __name__ == "__main__":
    main()
