from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertedPricePLN:
    price_in_source_currency: float
    currency: str
    currency_rate: float
    currency_rate_fetch_date: str
    price_in_pln: float


class PriceCurrencyConverterToPLN:
    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN:
        pass
