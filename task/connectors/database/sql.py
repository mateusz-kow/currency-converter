import logging
import os

from task.connectors.database.database_connector import DatabaseConnector
from task.currency_converter import ConvertedPricePLN
import sqlite3
from task.utils.config import SQL_DATABASE_NAME


logger = logging.getLogger(__name__)


class SQLDatabaseConnector(DatabaseConnector):
    def __init__(self, db_path: str = SQL_DATABASE_NAME):
        logger.debug("Initializing SQLDatabaseConnector...")
        self._db_path = db_path
        self._create_table()

    def _connect(self):
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        return sqlite3.connect(self._db_path)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS Exchanges (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            currency TEXT NOT NULL,
            rate FLOAT,
            price_in_pln FLOAT,
            date DATE
            )
            """)
            # "id": 3,
            # "currency": "eur",
            # "rate": 4.985,
            # "price_in_pln": 22.1,
            # "date": "2012-01-01"

    def save(self, entity: ConvertedPricePLN) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO Exchanges (currency, rate, price_in_pln, date)
            VALUES (?, ?, ?, ?)""",
                           (entity.currency,
                           entity.currency_rate,
                           entity.price_in_pln,
                           entity.currency_rate_fetch_date))

        return 0

    def get_all(self) -> list[...]:
        raise NotImplementedError

    def get_by_id(self, item_id: int) -> ...:
        raise NotImplementedError
