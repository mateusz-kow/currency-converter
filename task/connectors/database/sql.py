import logging

from task.connectors.database.database_connector import DatabaseConnector
from task.currency_converter import ConvertedPricePLN
import sqlite3
from task.utils.config import SQL_DATABASE_NAME

logger = logging.getLogger(__name__)
EXPECTED_EXTENSION = ".db"


class SQLDatabaseConnector(DatabaseConnector):

    def __init__(self, db_path: str = SQL_DATABASE_NAME):
        logger.debug("Initializing SQLDatabaseConnector...")
        super().__init__(db_path, ".db")

        self._db_path = db_path
        self._create_table()

    def _connect(self):
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

    def save(self, entity: ConvertedPricePLN) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO Exchanges (currency, rate, price_in_pln, date)
            VALUES (?, ?, ?, ?)""",
                           (entity.currency,
                            entity.currency_rate,
                            entity.price_in_pln,
                            str(entity.currency_rate_fetch_date)))

        return cursor.lastrowid

    def get_all(self) -> list[ConvertedPricePLN]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, currency, rate, price_in_pln, date FROM Exchanges")
            rows = cursor.fetchall()

        result = []
        for row in rows:
            item_id, currency, rate, price_in_pln, date = row
            price_in_source_currency = price_in_pln / rate if rate != 0 else 0
            result.append(ConvertedPricePLN(
                currency=currency,
                currency_rate=rate,
                currency_rate_fetch_date=date,
                price_in_pln=price_in_pln,
                price_in_source_currency=price_in_source_currency
            ))
        return result

    def get_by_id(self, item_id: int) -> ConvertedPricePLN:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT currency, rate, price_in_pln, date FROM Exchanges WHERE id = ?", (item_id,))
            row = cursor.fetchone()

        if row is None:
            logger.error(f"No record with id {item_id} found")

        currency, rate, price_in_pln, date = row
        price_in_source_currency = price_in_pln / rate if rate != 0 else 0

        return ConvertedPricePLN(
            currency=currency,
            currency_rate=rate,
            currency_rate_fetch_date=date,
            price_in_pln=price_in_pln,
            price_in_source_currency=price_in_source_currency
        )
