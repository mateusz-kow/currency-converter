from abc import abstractmethod, ABC
from datetime import date


class SourceConnector(ABC):

    @abstractmethod
    def get_date_and_rate(self, currency: str) -> tuple[date, float]:
        pass
