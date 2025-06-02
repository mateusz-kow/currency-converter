import os

JSON_DATABASE_NAME = "database.json"
SQL_DATABASE_NAME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database.db")
CURRENCY_RATES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   "example_currency_rates.json")
