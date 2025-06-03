import argparse
import logging

from task.utils.enums import Mode, Source

logger = logging.getLogger(__name__)


class ParsingError(Exception):
    pass


def currency(s: str) -> str:
    if len(s) != 3 and s.isalpha():
        raise argparse.ArgumentTypeError("Currency must be a 3-letter code like 'USD'")
    return s.upper()


def price(s: str) -> float:
    try:
        value = float(s)
        return round(value, 2)
    except ValueError:
        raise argparse.ArgumentTypeError("Amount must be a number like 12.34")


class MyParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description="Convert prices to PLN", exit_on_error=False)
        self.add_argument("--mode", default="dev", choices=("dev", "prod"),
                          help="dev - json database, prod - sqlite3 database")
        self.add_argument("--currency", required=True, type=currency,
                          help="currency of origin")
        self.add_argument("--source", required=True, choices=("api", "db"),
                          help="source of currency rate")
        self.add_argument("--price", required=True, type=price,
                          help="amount of money in the given currency")

    def get_args(self) -> tuple[str, float, Mode, Source]:
        try:
            args = self.parse_args()

            arg_currency = args.currency
            logger.debug(f"Given currency is {arg_currency}")

            arg_price = args.price
            logger.debug(f"Given price is {arg_price}")

            mode = args.mode
            logger.debug(f"Running in {mode} mode")
            if mode == "dev":
                arg_mode = Mode.DEV
            else:
                arg_mode = Mode.PROD

            source = args.source
            logger.debug(f"Data source is {source}")
            if source == "db":
                arg_source = Source.DATABASE
            else:
                arg_source = Source.API

            return arg_currency, arg_price, arg_mode, arg_source
        except Exception as e:
            raise ParsingError(e)
