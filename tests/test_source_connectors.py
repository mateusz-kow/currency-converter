import unittest
from datetime import date

from task.connectors.source.source_connector import SourceConnector
from task.connectors.source.remote.api_connector import ApiConnector
from task.connectors.source.local.file_reader import FileConnector


class TestApiConnector(unittest.TestCase):
    TEST_CLASS = ApiConnector

    def setUp(self):
        self._connector: SourceConnector = self.TEST_CLASS()

    def test_get_date_and_rate_valid_currency(self):
        currency = "EUR"  # or any currency your source supports
        d, rate = self._connector.get_date_and_rate(currency)

        self.assertIsInstance(d, date)
        self.assertIsInstance(rate, float)
        self.assertGreater(rate, 0.0)

    def test_get_date_and_rate_invalid_currency(self):
        with self.assertRaises(Exception):
            self._connector.get_date_and_rate("INVALID")

    def test_returned_date_is_not_in_future(self):
        currency = "CZK"
        d, _ = self._connector.get_date_and_rate(currency)
        self.assertLessEqual(d, date.today())

    def test_rate_consistency_between_calls(self):
        currency = "EUR"
        date1, rate1 = self._connector.get_date_and_rate(currency)
        date2, rate2 = self._connector.get_date_and_rate(currency)

        self.assertEqual(date1, date2)
        self.assertAlmostEqual(rate1, rate2, places=6)

    def test_supported_currency_loop(self):
        for currency in ["EUR", "CZK"]:
            with self.subTest(currency=currency):
                d, rate = self._connector.get_date_and_rate(currency)
                self.assertIsInstance(d, date)
                self.assertGreater(rate, 0.0)

    def test_invalid_currency_exception_has_currency_name(self):
        currency = "INVALID123"
        with self.assertRaises(Exception) as cm:
            self._connector.get_date_and_rate(currency)
        self.assertIn(currency, str(cm.exception))


class TestFileConnector(TestApiConnector):
    TEST_CLASS = FileConnector


if __name__ == "__main__":
    unittest.main()
