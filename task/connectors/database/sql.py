from task.connectors.database.database_connector import DatabaseConnector
from task.currency_converter import ConvertedPricePLN


class SQLDatabaseConnector(DatabaseConnector):
    def __init__(self):
        pass

    def save(self, entity: ConvertedPricePLN) -> int:
        raise NotImplementedError

    def get_all(self) -> list[...]:
        raise NotImplementedError

    def get_by_id(self, item_id: int) -> ...:
        raise NotImplementedError
