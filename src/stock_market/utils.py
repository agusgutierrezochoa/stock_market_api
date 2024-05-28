from fastapi.security.api_key import APIKeyHeader
from src.auth.database import get_db
from fastapi import Depends, HTTPException
from src.auth.models import User
from sqlalchemy.orm import Session

API_KEY_HEADER = APIKeyHeader(name='STOCK-INFO-API-Key', auto_error=False)


def auth_required(api_key: str = Depends(API_KEY_HEADER), db: Session = Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=403, detail="API key missing")
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return user
