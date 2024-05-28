import pytest
from unittest.mock import patch

from src.stock_market.stock_service import StockService


@pytest.fixture
def mock_response():
    return {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-05-27",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2024-05-27": {
                "1. open": "140.0000",
                "2. high": "142.0000",
                "3. low": "138.0000",
                "4. close": "141.0000",
                "5. volume": "1000000"
            },
            "2024-05-24": {
                "1. open": "138.0000",
                "2. high": "139.0000",
                "3. low": "136.0000",
                "4. close": "137.0000",
                "5. volume": "900000"
            }
        }
    }


@pytest.fixture
def stock_service():
    return StockService(function="TIME_SERIES_DAILY", symbol="IBM", size="compact")


def test_get_info(stock_service, mock_response):
    with patch.object(stock_service, 'call_vantage', return_value=mock_response):
        stock = stock_service.get_info()
        assert stock.symbol == "IBM"
        assert stock.open_price == "140.0000"
        assert stock.higher_price == "142.0000"
        assert stock.lower_price == "138.0000"
        assert stock.variation == "4.0"


def test_process_response(stock_service, mock_response):
    stock = stock_service.process_response(mock_response)
    assert stock.symbol == "IBM"
    assert stock.open_price == "140.0000"
    assert stock.higher_price == "142.0000"
    assert stock.lower_price == "138.0000"
    assert stock.variation == "4.0"


def test_process_response_no_time_series(stock_service):
    mock_response = {"Meta Data": {"2. Symbol": "IBM"}}
    with pytest.raises(ValueError, match=r"Time Series \(Daily\) not found in the response"):
        stock_service.process_response(mock_response)


def test_process_response_missing_close_price(stock_service):
    mock_response = {
        "Meta Data": {
            "2. Symbol": "IBM"
        },
        "Time Series (Daily)": {
            "2024-05-27": {
                "1. open": "140.0000",
                "2. high": "142.0000",
                "3. low": "138.0000",
                "4. close": "0",
                "5. volume": "1000000"
            },
            "2024-05-24": {
                "1. open": "138.0000",
                "2. high": "139.0000",
                "3. low": "136.0000",
                "4. close": "137.0000",
                "5. volume": "900000"
            }
        }
    }
    with pytest.raises(ValueError, match="Close price data is missing or invalid"):
        stock_service.process_response(mock_response)
