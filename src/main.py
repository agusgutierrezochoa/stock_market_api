from fastapi import FastAPI
from src.stock_market.router import router as stock_market_router
from src.auth.router import router as auth_router


app = FastAPI(title="Stock Market API Service")

app.include_router(stock_market_router)
app.include_router(auth_router)
