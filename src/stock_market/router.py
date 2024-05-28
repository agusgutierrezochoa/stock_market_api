from fastapi import APIRouter, Depends, HTTPException
from src.stock_market.schemas import StockMarketSchema, HTTPErrorResponse
from .utils import auth_required
from .stock_service import StockService
import circuitbreaker

router = APIRouter()


@router.get(
    "/stock_market_info/",
    response_model=StockMarketSchema,
    dependencies=[Depends(auth_required)],
    responses={
        200: {"model": StockMarketSchema},
        500: {"model": HTTPErrorResponse, "description": "Internal server error"},
    },
)
def get_stock_market_info(symbol: str, function: str = 'TIME_SERIES_DAILY') -> dict:
    try:
        stock_service = StockService(function=function, symbol=symbol)
        info = stock_service.get_info()
    except circuitbreaker.CircuitBreakerError as e:
        raise HTTPException(
            status_code=503,
            detail={
                "error": 500,
                "message": f"Circuit breaker active: {e}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": 500,
                "message": f"Internal server error: {e.args}"
            }
        )

    return {"stock": info}
