from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

from task.connectors.database.database_connector import DatabaseConnector
from task.currency_converter import ConvertedPricePLN
from task.utils.config import SQL_DATABASE_NAME

import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class Exchange(Base):
    __tablename__ = "Exchanges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String, nullable=False)
    rate = Column(Float)
    price_in_pln = Column(Float)
    date = Column(Date)


class SQLDatabaseConnector(DatabaseConnector):

    def __init__(self, db_path: str = SQL_DATABASE_NAME):
        super().__init__(db_path, ".db")
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def save(self, entity: ConvertedPricePLN) -> int:
        exchange = Exchange(
            currency=entity.currency,
            rate=entity.currency_rate,
            price_in_pln=entity.price_in_pln,
            date=entity.currency_rate_fetch_date
        )
        self.session.add(exchange)
        self.session.commit()
        return exchange.id

    def get_all(self) -> list[ConvertedPricePLN]:
        exchanges = self.session.query(Exchange).all()
        return [
            ConvertedPricePLN(
                currency=ex.currency,
                currency_rate=ex.rate,
                currency_rate_fetch_date=ex.date,
                price_in_pln=ex.price_in_pln,
                price_in_source_currency=(ex.price_in_pln / ex.rate if ex.rate else 0)
            )
            for ex in exchanges
        ]

    def get_by_id(self, item_id: int) -> ConvertedPricePLN:
        ex = self.session.query(Exchange).filter_by(id=item_id).first()
        if not ex:
            logger.error(f"No record with id {item_id} found")
            raise KeyError(f"Item with id {item_id} not found.")
        return ConvertedPricePLN(
            currency=ex.currency,
            currency_rate=ex.rate,
            currency_rate_fetch_date=ex.date,
            price_in_pln=ex.price_in_pln,
            price_in_source_currency=(ex.price_in_pln / ex.rate if ex.rate else 0)
        )

    def close(self):
        self.session.close()
        self.engine.dispose()
