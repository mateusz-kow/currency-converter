from task.connectors.source.remote.api_connector import ApiConnector
from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sql import SQLDatabaseConnector
from task.connectors.source.local.file_reader import FileConnector
from task.currency_converter import Source, Mode

DATABASE_CONNECTORS = {
    Mode.PROD: SQLDatabaseConnector,
    Mode.DEV: JsonFileDatabaseConnector}
SOURCE_CONNECTORS = {
    Source.API: ApiConnector,
    Source.DATABASE: FileConnector
}
