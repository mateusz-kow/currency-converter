import logging
from datetime import datetime, date
import requests
from requests.exceptions import ConnectionError as RequestsConnectionError

from task.connectors.source.source_connector import SourceConnector

logger = logging.getLogger(__name__)


class ApiConnector(SourceConnector):
    def get_date_and_rate(self, currency: str) -> tuple[date, float]:
        logger.debug("Initializing remote request...")
        try:
            request = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json")
            status_code = request.status_code
            if status_code == 404:
                logger.error(f"{status_code} Currency not found")
                raise ValueError(f"{status_code} Currency not found")
            if status_code != 200:
                logger.error(f"Request failed with code {status_code}")
                raise ValueError(f"{status_code} Failed to get current rate")
            logger.debug(f"Request completed successfully with code {status_code}")

            result: dict = request.json()
            logger.debug(f"Received response of {result}")
            rates: dict = result["rates"][0]

            rate = float(rates["mid"])
            date_str = rates["effectiveDate"]
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            return formatted_date, rate

        except RequestsConnectionError:
            logger.error("Network error while connecting to NBP API")
            raise ConnectionError("No internet connection")
        except Exception:
            raise
