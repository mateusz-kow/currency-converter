import unittest

from task.currency_converter import PriceCurrencyConverterToPLN, Source


class TestApiConverter(unittest.TestCase):
    def setUp(self):
        self._converter = PriceCurrencyConverterToPLN(Source.API)

    def test_pln(self):
        entity = self._converter.convert_to_pln(currency="PLN", price=100)
        assert entity.price_in_pln == 100
        assert entity.price_in_source_currency == 100
        assert entity.currency == "PLN"
        assert entity.currency_rate == 1

    def test_eur(self):
        entity = self._converter.convert_to_pln(currency="EUR", price=12.34)
        assert entity.price_in_source_currency == 12.34

    def test_czk(self):
        entity = self._converter.convert_to_pln(currency="CZK", price=43.90)
        assert entity.price_in_source_currency == 43.90


class TestDBConverter(TestApiConverter):
    def setUp(self):
        self._converter = PriceCurrencyConverterToPLN(Source.DATABASE)


if __name__ == "__main__":
    unittest.main()
