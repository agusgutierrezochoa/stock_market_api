import requests
from .constants import (
    VANTAGE_URL,
    TIME_SERIES_KEY,
    INFORMATION,
    CLOSE_KEY,
    SYMBOL_KEY,
    OPEN_KEY,
    HIGH_KEY,
    LOW_KEY
)
from .schemas import Stock
from .circuit_breaker import VantageCircuitBreaker
import os

VANTAGE_API_KEY = os.environ.get('VANTAGE_API_KEY', '')


class StockService:

    def __init__(self, function: str, symbol: str, size: str = "compact") -> None:
        self.function = function
        self.size = size
        self.symbol = symbol

    def get_info(self) -> Stock:
        result = self.call_vantage()

        stock = self.process_response(result)

        return stock

    @VantageCircuitBreaker()
    def call_vantage(self) -> dict:
        url = VANTAGE_URL.format(
            function=self.function,
            symbol=self.symbol,
            size=self.size,
            api_key=VANTAGE_API_KEY
        )
        result = requests.get(url)
        result.raise_for_status()
        return result.json()

    def process_response(self, result: dict) -> Stock:
        try:
            time_series = result.get(TIME_SERIES_KEY)
            if not time_series and INFORMATION in result:
                raise ValueError(str("Vantage: " + result.get(INFORMATION)))
            elif not time_series:
                raise ValueError("Time Series (Daily) not found in the response")
            last_two_days = sorted(time_series.keys(), reverse=True)[:2]
            last_day_close = float(time_series[last_two_days[0]].get(CLOSE_KEY, 0))
            before_last_day_close = float(time_series[last_two_days[1]].get(CLOSE_KEY, 0))

            if last_day_close == 0 or before_last_day_close == 0:
                raise ValueError("Close price data is missing or invalid")

            variation = last_day_close - before_last_day_close

            return Stock(
                symbol=result.get('Meta Data').get(SYMBOL_KEY),
                open_price=time_series.get(last_two_days[0]).get(OPEN_KEY),
                higher_price=time_series.get(last_two_days[0]).get(HIGH_KEY),
                lower_price=time_series.get(last_two_days[0]).get(LOW_KEY),
                variation=str(variation),
            )
        except Exception as e:
            raise e
