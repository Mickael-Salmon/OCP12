# main.py
from views.menu import main as menu_main

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

if __name__ == "__main__":
    menu_main()
