import logging
import requests

from task.connectors.source.source_connector import SourceConnector

logger = logging.getLogger()


class ApiConnector(SourceConnector):
    @staticmethod
    def get_date_and_rate(currency: str) -> (str, float):
        logger.debug("Initializing remote request...")
        try:
            request = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json")
            status_code = request.status_code
            if status_code == 404:
                logger.error(f"{status_code} Currency not found")
                raise NotImplementedError(f"{status_code} Currency not found")
            if status_code != 200:
                logger.error(f"Request failed with code {status_code}")
                raise NotImplementedError(f"Invalid status code {status_code}")
            logger.debug(f"Request completed successfully with code {status_code}")

            result: dict = request.json()
            logger.debug(f"Received response of {result}")
            rates: dict = result["rates"][0]

            rate = float(rates["mid"])
            date = rates["effectiveDate"]

            return date, rate

        except ConnectionError:
            raise ConnectionError("Check your internet connection")
        except Exception:
            raise
