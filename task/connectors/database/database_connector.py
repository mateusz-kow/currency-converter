import logging
import os
from abc import ABC, abstractmethod

from task.currency_converter import ConvertedPricePLN

logger = logging.getLogger(__name__)


class DatabaseConnector(ABC):
    def __init__(self, db_path: str, expected_ext: str = ""):
        _, ext = os.path.splitext(db_path)
        if ext != expected_ext:
            raise ValueError(f"Invalid file format: {os.path.basename(db_path)}. "
                             f"Expected a {expected_ext} file, got {ext}")

        if not os.path.exists(db_path):
            logger.warning(f"Path doesn't exist: {db_path}")
            db_dir = os.path.dirname(db_path)
            if not os.path.exists(db_dir):
                logger.debug(f"Creating path {db_dir}...")
                os.makedirs(db_dir)

    @abstractmethod
    def save(self, entity: ConvertedPricePLN) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[ConvertedPricePLN]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> ConvertedPricePLN:
        pass
