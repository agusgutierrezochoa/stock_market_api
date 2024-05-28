import requests
from .constants import VANTAGE_URL
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
            time_series = result.get('Time Series (Daily)')
            if not time_series:
                raise ValueError("Time Series (Daily) not found in the response")
            last_two_days = sorted(time_series.keys(), reverse=True)[:2]
            last_day_close = float(time_series[last_two_days[0]].get('4. close', 0))
            before_last_day_close = float(time_series[last_two_days[1]].get('4. close', 0))

            if last_day_close == 0 or before_last_day_close == 0:
                raise ValueError("Close price data is missing or invalid")

            variation = last_day_close - before_last_day_close

            return Stock(
                symbol=result.get('Meta Data').get('2. Symbol'),
                open_price=time_series.get(last_two_days[0]).get('1. open'),
                higher_price=time_series.get(last_two_days[0]).get('2. high'),
                lower_price=time_series.get(last_two_days[0]).get('3. low'),
                variation=str(variation),
            )
        except Exception as e:
            raise e
