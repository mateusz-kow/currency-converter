import json
import os
import unittest
from datetime import datetime, timedelta

from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sql import SQLDatabaseConnector
from task.currency_converter import ConvertedPricePLN
from tests import TEST_PATH
import random
import gc
from filelock import FileLock


class TestJsonFileDatabaseConnector(unittest.TestCase):
    TEST_CLASS = JsonFileDatabaseConnector
    TEST_DB_PATH = os.path.join(TEST_PATH, "test_database.json")
    LOCK_PATH = TEST_PATH + ".lock"

    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_PATH, exist_ok=True)
        cls._lock = FileLock(cls.LOCK_PATH)
        cls._connector = None

    @classmethod
    def tearDownClass(cls):
        with cls._lock:
            if os.path.exists(cls.TEST_DB_PATH):
                os.remove(cls.TEST_DB_PATH)
            os.rmdir(TEST_PATH)

    def setUp(self):
        self.tearDown()
        with self._lock:
            with open(self.TEST_DB_PATH, "w") as file:
                if self.TEST_CLASS == JsonFileDatabaseConnector:
                    json.dump({}, file)
            self._connector = self.TEST_CLASS(self.TEST_DB_PATH)

    def tearDown(self):
        with self._lock:
            if self._connector and hasattr(self._connector, "close"):
                self._connector.close()
            self._connector = None
            gc.collect()

            if os.path.exists(self.TEST_DB_PATH):
                os.remove(self.TEST_DB_PATH)

    @staticmethod
    def _create_entity() -> ConvertedPricePLN:
        currency = random.choice(["USD", "EUR", "PLN", "CHF", "CZK"])
        currency_rate = round(random.uniform(0.5, 6.0), 4)
        price_in_source_currency = round(random.uniform(1, 1000), 2)
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
        self.assertEqual(retrieved.currency_rate, entity.currency_rate)
        self.assertEqual(retrieved.price_in_pln, entity.price_in_pln)
        self.assertEqual(str(retrieved.currency_rate_fetch_date), str(entity.currency_rate_fetch_date))

    def test_get_all(self):
        entities = [self._create_entity() for _ in range(3)]
        for entity in entities:
            self._connector.save(entity)

        all_items = self._connector.get_all()
        self.assertEqual(len(all_items), 3)

        for original, retrieved in zip(entities, all_items):
            self.assertEqual(retrieved.currency, original.currency)
            self.assertEqual(retrieved.currency_rate, original.currency_rate)
            self.assertEqual(retrieved.price_in_pln, original.price_in_pln)

    def test_get_by_id_nonexistent(self):
        with self.assertRaises(KeyError):
            self._connector.get_by_id("nonexistent-id")

    def test_save_multiple_unique_ids(self):
        ids = set()
        for _ in range(10):
            entity = self._create_entity()
            item_id = self._connector.save(entity)
            self.assertNotIn(item_id, ids)
            ids.add(item_id)
        self.assertEqual(len(ids), 10)

    def test_persistence_between_instances(self):
        entity = self._create_entity()
        item_id = self._connector.save(entity)
        entity = self._connector.get_by_id(item_id)

        connector = self.TEST_CLASS(self.TEST_DB_PATH)
        retrieved = connector.get_by_id(item_id)

        if hasattr(connector, "close"):
            connector.close()

        self.assertEqual(str(retrieved), str(entity))


class TestSQLDatabaseConnector(TestJsonFileDatabaseConnector):
    TEST_CLASS = SQLDatabaseConnector
    TEST_DB_PATH = os.path.join(TEST_PATH, "test_database.db")


if __name__ == "__main__":
    unittest.main()
