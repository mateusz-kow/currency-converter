import logging
from dataclasses import dataclass
from datetime import date, datetime

from task.connectors.source.source_connector import SourceConnector
from task.utils.enums import Source

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: date
    price_in_pln: float

    def __str__(self):
        return (f"{self.price_in_source_currency} {self.currency} = {self.price_in_pln} PLN "
                f"| rate: {self.currency_rate} | date: {self.currency_rate_fetch_date}")


class ConversionError(Exception):
    pass


class PriceCurrencyConverterToPLN:
    def __init__(self, source: Source):
        from task.utils.constants import get_source_connector

        logger.info("Initializing PriceCurrencyConverterToPLN...")
        self._source_connector: SourceConnector = get_source_connector(source)()

    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN:
        logger.info(f"Converting {price} {currency} to PLN...")
        try:
            if currency == "PLN":
                result_date = str(datetime.now().date())
                rate = 1.00
            else:
                result_date, rate = self._source_connector.get_date_and_rate(currency=currency)

            converted_price = ConvertedPricePLN(price, currency, rate, result_date, round(price * rate, 2))
            logger.debug(f"Initialized ConvertedPricePLN as: {str(converted_price)}")

            return converted_price
        except Exception as e:
            raise ConversionError(f"Failed to convert {price} {currency} to PLN: {e}")
