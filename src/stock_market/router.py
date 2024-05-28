from fastapi import APIRouter
from src.stock_market.schemas import StockMarketSchema

router = APIRouter()


@router.get("/stock_market_info/", response_model=StockMarketSchema)
def get_stock_market_info():
    return {"foo": "bar"}
