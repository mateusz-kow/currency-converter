from abc import abstractmethod, ABC


class SourceConnector(ABC):
    @staticmethod
    @abstractmethod
    def get_date_and_rate(currency: str):
        pass
