import json
import logging

from task.utils.config import JSON_DATABASE_NAME
from task.connectors.database.database_connector import DatabaseConnector
from task.currency_converter import ConvertedPricePLN


logger = logging.getLogger(__name__)


class JsonFileDatabaseConnector(DatabaseConnector):
    def __init__(self, db_path: str = JSON_DATABASE_NAME) -> None:
        logger.debug("Initializing JsonDatabaseConnector...")
        self._db_path = db_path
        self._data = self._read_data(db_path)

    @staticmethod
    def _read_data(db_path: str = JSON_DATABASE_NAME) -> dict:
        with open(db_path, "r") as file:
            return json.load(file)

    def save(self, entity: ConvertedPricePLN) -> int:
        logger.debug(f"Saving data to {self._db_path}...")
        item_id = max(map(int, self._data.keys())) + 1

        self._data[item_id] = {
            "id": item_id,
            "currency": entity.currency,
            "rate": entity.currency_rate,
            "price_in_pln": entity.price_in_pln,
            "date": entity.currency_rate_fetch_date
        }
        with open(self._db_path, "w") as file:
            json.dump(self._data, file, indent = "\t")

        return item_id

    def get_all(self) -> list[...]:
        return [k for k in self._data.values()]

    def get_by_id(self, item_id: int) -> ConvertedPricePLN:
        if item_id not in self._data.keys():
            raise AttributeError

        item = self._data[item_id]
        currency = item["currency"]
        currency_rate = item["rate"]
        currency_rate_fetch_date = item["date"]
        price_in_pln = item["price_in_pln"]
        price_in_source_currency = price_in_pln / currency_rate

        return ConvertedPricePLN(currency=currency,
                                 currency_rate=currency_rate,
                                 currency_rate_fetch_date=currency_rate_fetch_date,
                                 price_in_pln=price_in_pln,
                                 price_in_source_currency=price_in_source_currency)
