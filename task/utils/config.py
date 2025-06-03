import os

JSON_DATABASE_NAME = "database.json"
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SQL_DATABASE_NAME = os.path.join(PROJECT_PATH, "database.db")
CURRENCY_RATES_FILE = os.path.join(PROJECT_PATH, "example_currency_rates.json")
