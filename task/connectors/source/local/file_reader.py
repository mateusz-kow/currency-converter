import json
import logging

from task.utils.config import CURRENCY_RATES_FILE
from task.connectors.source.source_connector import SourceConnector

logger = logging.getLogger(__name__)


class FileConnector(SourceConnector):
    def __init__(self, file: str = CURRENCY_RATES_FILE):
        logger.info("Initializing FileConnector...")
        super().__init__()
        self._file = file

    def get_date_and_rate(self, currency: str) -> (str, float):
        logger.debug(f"Loading data and rate on currency {currency}")
        try:
            with open(self._file, 'r') as file:
                info = json.load(file)

            if currency in info:
                rates_list = info[currency]
                chosen_rate = rates_list[0]
                return chosen_rate["date"], chosen_rate["rate"]

            else:
                raise ValueError(f"Currency {currency} not present in the {CURRENCY_RATES_FILE} file")
        except:
            raise
