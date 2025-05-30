from dataclasses import dataclass
import logging
from datetime import datetime
from enum import Enum

from task.connectors.source.source_connector import SourceConnector

logger = logging.getLogger(__name__)


class ConversionError(Exception):
    pass


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float

    def __str__(self):
        return (f"{self.price_in_source_currency} {self.currency} = {self.price_in_pln} PLN "
                f"| rate: {self.currency_rate} | date: {self.currency_rate_fetch_date}")


class Mode(Enum):
    DEV = 1
    PROD = 2


class Source(Enum):
    API = 1
    DATABASE = 2


class PriceCurrencyConverterToPLN:
    def __init__(self, source: Source):
        from task.utils.dicts import SOURCE_CONNECTORS
        if source not in SOURCE_CONNECTORS:
            raise NotImplementedError(f"Source {source} is not implemented yet")
        self._source_connector: SourceConnector = SOURCE_CONNECTORS[source]()

    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN:
        try:
            logger.debug(f"Converting {price} {currency} to PLN...")

            if currency == "PLN":
                date = str(datetime.now().date())
                rate = 1.00
            else:
                date, rate = self._source_connector.get_date_and_rate(currency=currency)

            converted_price = ConvertedPricePLN(price, currency, rate, date, round(price * rate, 2))

            return converted_price
        except Exception as e:
            raise ConversionError(e)
