from abc import ABC, abstractmethod
from task.currency_converter import ConvertedPricePLN


class DatabaseConnector(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def save(self, entity: ConvertedPricePLN) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[...]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> ...:
        pass
