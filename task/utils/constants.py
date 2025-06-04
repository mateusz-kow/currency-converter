from task.connectors.database.database_connector import DatabaseConnector
from task.connectors.database.json import JsonFileDatabaseConnector
from task.connectors.database.sql import SQLDatabaseConnector
from task.connectors.source.local.file_reader import FileReader
from task.connectors.source.remote.api_connector import ApiConnector
from task.connectors.source.source_connector import SourceConnector
from task.utils.enums import Mode, Source

DATABASE_CONNECTORS: dict[Mode, type[DatabaseConnector]] = {
    Mode.PROD: SQLDatabaseConnector,
    Mode.DEV: JsonFileDatabaseConnector}
SOURCE_CONNECTORS: dict[Source, type[SourceConnector]] = {
    Source.API: ApiConnector,
    Source.DATABASE: FileReader
}


def get_database_connector(mode: Mode):
    if mode not in DATABASE_CONNECTORS.keys():
        raise NotImplementedError(f"Mode {mode} not implemented")
    return DATABASE_CONNECTORS[mode]


def get_source_connector(source: Source):
    if source not in SOURCE_CONNECTORS.keys():
        raise NotImplementedError(f"Source {source} not implemented")
    return SOURCE_CONNECTORS[source]
