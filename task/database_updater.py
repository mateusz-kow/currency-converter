import logging

from task.currency_converter import Mode, ConvertedPricePLN
from task.connectors.database.database_connector import DatabaseConnector

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    pass


class DatabaseUpdater:
    def __init__(self, mode: Mode, db_path: str = None):
        logger.debug("Initializing DatabaseUpdater...")
        from task.utils.dicts import DATABASE_CONNECTORS
        if mode not in DATABASE_CONNECTORS:
            logger.error(f"Mode {mode} isn't implemented yet")
            raise NotImplementedError(f"Mode {mode} isn't implemented yet")
        self._connector: DatabaseConnector = DATABASE_CONNECTORS[mode](db_path)

    def update_database(self, converted_price: ConvertedPricePLN):
        try:
            self._connector.save(converted_price)
        except Exception as e:
            raise DatabaseError(e)
