import json
import logging
import os.path
from datetime import date, datetime

from task.connectors.source.source_connector import SourceConnector
from task.utils.config import CURRENCY_RATES_FILE


class InvalidCurrencyDataError(Exception):
    pass


logger = logging.getLogger(__name__)


class FileReader(SourceConnector):
    def __init__(self, file: str = CURRENCY_RATES_FILE):
        logger.info("Initializing FileConnector...")
        if not os.path.exists(file):
            raise ValueError(f"Path doesn't exist: {file}")

        _, ext = os.path.splitext(file)
        if ext != ".json":
            raise ValueError(f"Invalid file format: {os.path.basename(file)}. Expected a .json file, got {ext}")
        super().__init__()
        self._file = file
        self._filename = os.path.basename(file)

    def get_date_and_rate(self, currency: str) -> tuple[date, float]:
        logger.debug(f"Loading data and rate on currency {currency}")
        try:
            with open(self._file, 'r') as file:
                content = json.load(file)

            if currency in content:
                rates_list: list = content[currency]
                if not rates_list:
                    raise InvalidCurrencyDataError(f"No rates found for currency {currency} in {self._filename}")

                chosen_rate = max(rates_list, key=lambda r: datetime.strptime(r["date"], "%Y-%m-%d").date())
                date_str = chosen_rate["date"]
                formatted_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                rate = chosen_rate["rate"]
                logger.debug(f"Date: {formatted_date}, rate: {rate}")
                return formatted_date, rate

            else:
                raise InvalidCurrencyDataError(f"Currency {currency} not present in the {self._filename} file")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Data error while reading '{self._file}': {e}")
            raise ValueError(f"Incorrect JSON file structure ({self._filename})") from e
        except InvalidCurrencyDataError as e:
            logger.error(f"Couldn't convert currency from file '{self._file}': {e}")
            raise
        except OSError as e:
            logger.error(f"Couldn't open file '{self._file}': {e}")
            raise OSError(f"Couldn't open file '{self._filename}'") from e
        except Exception as e:
            logger.error(f"Unexpected error reading '{self._file}': {e}")
            raise
