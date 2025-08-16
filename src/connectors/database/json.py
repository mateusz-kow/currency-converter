import json
import logging

from task.connectors.database.database_connector import DatabaseConnector
from task.utils.config import JSON_DATABASE_NAME
from task.currency_converter import ConvertedPricePLN


logger = logging.getLogger(__name__)


class JsonFileDatabaseConnector(DatabaseConnector):
    def __init__(self, db_path: str = JSON_DATABASE_NAME) -> None:
        logger.debug("Initializing JsonDatabaseConnector...")
        super().__init__(db_path, ".json")

        self._db_path = db_path
        self._data = self._read_data(db_path)

    @staticmethod
    def _read_data(db_path: str = JSON_DATABASE_NAME) -> dict:
        with open(db_path, "r") as file:
            return json.load(file)

    def save(self, entity: ConvertedPricePLN) -> int:
        logger.debug(f"Saving data to {self._db_path}...")
        item_id = max(map(int, self._data.keys()), default=0) + 1
        key = str(item_id)

        self._data[key] = {
            "id": item_id,
            "currency": entity.currency,
            "rate": entity.currency_rate,
            "price_in_pln": entity.price_in_pln,
            "date": str(entity.currency_rate_fetch_date)
        }
        with open(self._db_path, "w") as file:
            json.dump(self._data, file, indent=4)

        return item_id

    def get_all(self) -> list[ConvertedPricePLN]:
        results = []
        for k in self._data.keys():
            try:
                results.append(self.get_by_id(int(k)))
            except Exception as e:
                logger.error(f"Couldn't load item {k}: {e}")
        return results

    def get_by_id(self, item_id: int) -> ConvertedPricePLN:
        key = str(item_id)
        if key not in self._data:
            raise KeyError(f"Item with id {item_id} not found. {self._data}")

        item = self._data[key]
        currency = item["currency"]
        currency_rate = item["rate"]
        currency_rate_fetch_date = item["date"]
        price_in_pln = item["price_in_pln"]
        price_in_source_currency = price_in_pln / currency_rate if currency_rate != 0 else 0

        return ConvertedPricePLN(
            currency=currency,
            currency_rate=currency_rate,
            currency_rate_fetch_date=currency_rate_fetch_date,
            price_in_pln=price_in_pln,
            price_in_source_currency=price_in_source_currency
        )
