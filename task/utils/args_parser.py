import argparse
import logging

from task.currency_converter import Mode, Source

logger = logging.getLogger(__name__)


class ParsingError(Exception):
    pass


def currency(s: str):
    if len(s) != 3:
        raise TypeError()
    return s


class MyParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description="Convert prices to PLN")
        self.add_argument("--mode", default="dev", choices=("dev", "prod"),
                          help="dev - json database, prod - sqlite3 database")
        self.add_argument("--currency", required=True, type=currency,
                          help="currency of origin")
        self.add_argument("--source", required=True, choices=("api", "db"),
                          help="source of currency rate")
        self.add_argument("--amount", required=True, type=int,
                          help="amount of money in the given currency")

    def error(self, message):
        raise ParsingError(message)

    def get_args(self) -> (str, float, Mode, Source):
        try:
            args = self.parse_args()

            arg_currency = args.currency.upper()
            if len(arg_currency) != 3:
                logger.error(f"Currency {arg_currency} has invalid format")
                raise NotImplementedError
            logger.debug(f"Given currency is {arg_currency}")

            arg_price = float(args.amount)

            if len(str(arg_price).split('.')[1]) > 2:
                arg_price = round(arg_price, 2)
                logger.warning(f"Rounding the given price to {arg_price}")
            logger.debug(f"Given price is {arg_price}")

            arg_mode = args.mode
            logger.debug(f"Running in {arg_mode} mode")
            if arg_mode == "dev":
                arg_mode = Mode.DEV
            else:
                arg_mode = Mode.PROD

            arg_source = args.source
            logger.debug(f"Data source is {arg_source}")
            if arg_source == "db":
                arg_source = Source.DATABASE
            else:
                arg_source = Source.API

            return arg_currency, arg_price, arg_mode, arg_source
        except Exception as e:
            raise ParsingError(e)
