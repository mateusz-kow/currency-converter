import sys
import logging
import traceback

from task.utils import setup_logging
from task.currency_converter import PriceCurrencyConverterToPLN, ConversionError
from task.utils.args_parser import MyParser, ParsingError
from task.database_updater import DatabaseUpdater, DatabaseError

logger = logging.getLogger(__name__)


def _handle_unexpected_error(error: Exception):
    logger.error(error)
    logger.error(traceback.format_exc())
    sys.stderr.write(f"Unexpected error occured: {error}")


try:
    logger.info("Parsing arguments...")
    parser = MyParser()
    currency, price, mode, source = parser.get_args()

    logger.info("Converting price...")
    converter = PriceCurrencyConverterToPLN(source)
    converted_price = converter.convert_to_pln(currency=currency, price=price)

    sys.stdout.write(f"{str(converted_price)}\n")
    logger.info(f"Converted price: {str(converted_price)}")

except ParsingError as e:
    sys.stderr.write(f"{str(e)}\n")
    sys.exit(2)
except ConversionError as e:
    logger.error(e)
    logger.error(traceback.format_exc())
    sys.stderr.write("Failed to convert the price\n")
except Exception as e:
    _handle_unexpected_error(e)

try:
    logger.info("Updating database...")
    database_updater = DatabaseUpdater(mode)
    database_updater.update_database(converted_price)

    sys.stdout.write("Database updated successfully\n")
    logger.info("Database updated successfully")

except NameError as e:
    logger.error(e)
    logger.error(traceback.format_exc())
    sys.stderr.write("Failed to update database\n")
except DatabaseError as e:
    logger.error(e)
    logger.error(traceback.format_exc())
    sys.stderr.write("Failed to update database\n")
except Exception as e:
    logger.error(e)
    logger.error(traceback.format_exc())
    sys.stderr.write("Failed to update database\n")
