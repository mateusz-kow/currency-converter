import os
import unittest
from datetime import datetime, timedelta
import random
import json
import gc
from filelock import FileLock
from task.currency_converter import ConvertedPricePLN
from task.connectors.database.json import JsonFileDatabaseConnector
from tests import TEST_PATH

TEST_JSON_PATH = os.path.join(TEST_PATH, "test_database.json")
LOCK_PATH = TEST_PATH + ".lock"


class TestJsonFileDatabaseConnector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_PATH, exist_ok=True)
        cls._lock = FileLock(LOCK_PATH)

    @classmethod
    def tearDownClass(cls):
        with cls._lock:
            if os.path.exists(TEST_JSON_PATH):
                os.remove(TEST_JSON_PATH)

            os.rmdir(TEST_PATH)

    def setUp(self):
        gc.collect()
        with self._lock:
            if os.path.exists(TEST_JSON_PATH):
                os.remove(TEST_JSON_PATH)
            with open(TEST_JSON_PATH, "w") as f:
                json.dump({}, f)
            self._connector = JsonFileDatabaseConnector(TEST_JSON_PATH)

    def tearDown(self):
        self._connector = None
        gc.collect()
        with self._lock:
            if os.path.exists(TEST_JSON_PATH):
                os.remove(TEST_JSON_PATH)

    @staticmethod
    def _create_entity() -> ConvertedPricePLN:
        currency = random.choice(["USD", "EUR", "PLN", "CHF", "CZK"])
        currency_rate = round(random.uniform(0.5, 6.0), 4)
        price_in_source_currency = round(random.uniform(10, 1000), 2)
        price_in_pln = round(currency_rate * price_in_source_currency, 2)

        days_ago = random.randint(0, 365)
        fetch_date = (datetime.now() - timedelta(days=days_ago)).date()

        return ConvertedPricePLN(
            currency=currency,
            currency_rate=currency_rate,
            currency_rate_fetch_date=fetch_date,
            price_in_pln=price_in_pln,
            price_in_source_currency=price_in_source_currency
        )

    def test_save_and_get_by_id(self):
        entity = self._create_entity()
        item_id = self._connector.save(entity)
        retrieved = self._connector.get_by_id(item_id)

        self.assertEqual(retrieved.currency, entity.currency)
        self.assertAlmostEqual(retrieved.currency_rate, entity.currency_rate)
        self.assertAlmostEqual(retrieved.price_in_pln, entity.price_in_pln)
        self.assertEqual(str(retrieved.currency_rate_fetch_date), str(entity.currency_rate_fetch_date))

    def test_get_all(self):
        entities = [self._create_entity() for _ in range(3)]
        for entity in entities:
            self._connector.save(entity)

        all_items = self._connector.get_all()
        self.assertEqual(len(all_items), 3)

        for original, retrieved in zip(entities, all_items):
            self.assertEqual(retrieved.currency, original.currency)
            self.assertAlmostEqual(retrieved.currency_rate, original.currency_rate)
            self.assertAlmostEqual(retrieved.price_in_pln, original.price_in_pln)

    def test_get_by_id_not_found(self):
        with self.assertRaises(KeyError):
            self._connector.get_by_id(9999)


if __name__ == "__main__":
    unittest.main()
