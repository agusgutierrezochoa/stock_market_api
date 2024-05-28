from pydantic import BaseModel


class Stock(BaseModel):
    symbol: str
    open_price: str
    higher_price: str
    lower_price: str
    variation: str


class StockMarketSchema(BaseModel):

    stock: Stock


class HTTPErrorResponse(BaseModel):
    error: int
    message: str
