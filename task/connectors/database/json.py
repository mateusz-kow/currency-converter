import json
from ...config import JSON_DATABASE_NAME


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            return json.load(file)

    def save(self, entity: ...) -> int:
        raise NotImplementedError()

    def get_all(self) -> list[...]:
        raise NotImplementedError()

    def get_by_id(self) -> ...:
        raise NotImplementedError()

