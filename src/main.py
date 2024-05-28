from fastapi import FastAPI, Request
from src.stock_market.router import router as stock_market_router
from src.auth.router import router as auth_router
from src.logging_config import logger

app = FastAPI(title="Stock Market API Service")

app.include_router(stock_market_router)
app.include_router(auth_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
