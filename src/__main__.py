import sys
import logging

from task.currency_converter import PriceCurrencyConverterToPLN, ConversionError
from task.utils.args_parser import MyParser, ParsingError
from task.database_updater import DatabaseUpdater, DatabaseError

logger = logging.getLogger(__name__)


def _handle_unexpected_error(error: Exception, code: int = 1) -> None:
    logger.exception(error)
    sys.stderr.write(f"{str(error)}\n")
    sys.exit(code)


mode = None
converted_price = None

try:
    logger.info("Parsing arguments...")
    parser = MyParser()
    currency, price, mode, source = parser.get_args()

    logger.info(f"Starting conversion: {price} {currency} from {source}")
    converter = PriceCurrencyConverterToPLN(source)
    converted_price = converter.convert_to_pln(currency=currency, price=price)

    sys.stdout.write(f"{str(converted_price)}\n")
    logger.info(f"Converted price: {str(converted_price)}")

except ParsingError as e:
    _handle_unexpected_error(e, 2)
except ConversionError as e:
    _handle_unexpected_error(e, 3)
except Exception as e:
    _handle_unexpected_error(e)

if mode is not None and converted_price is not None:
    try:
        logger.info("Updating database...")
        database_updater = DatabaseUpdater(mode)
        database_updater.update_database(converted_price)

        sys.stdout.write("Database updated successfully\n")
        logger.info("Database updated successfully")

    except DatabaseError as e:
        sys.stderr.write("Failed to update database\n")
        _handle_unexpected_error(e, 4)
    except Exception as e:
        sys.stderr.write("Failed to update database\n")
        _handle_unexpected_error(e)
