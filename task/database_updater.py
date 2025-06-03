import logging

from task.currency_converter import ConvertedPricePLN
from task.connectors.database.database_connector import DatabaseConnector
from task.utils.enums import Mode

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    pass


class DatabaseUpdater:
    def __init__(self, mode: Mode, db_path: str = None):
        from task.utils.constants import get_database_connector

        logger.debug("Initializing DatabaseUpdater...")
        connector_cls = get_database_connector(mode)
        if db_path:
            self._connector: DatabaseConnector = connector_cls(db_path)
        else:
            self._connector: DatabaseConnector = connector_cls()

    def update_database(self, converted_price: ConvertedPricePLN):
        try:
            self._connector.save(converted_price)
        except Exception as e:
            raise DatabaseError(e)
