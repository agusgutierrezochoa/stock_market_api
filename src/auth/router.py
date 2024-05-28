from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db
from sqlalchemy.exc import IntegrityError

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api")


@router.post(
    "/users/",
    response_model=schemas.User,
    responses={
        201: {"model": schemas.User},
        409: {"model": schemas.HTTPErrorResponse, "description": "User already exists"},
        500: {"model": schemas.HTTPErrorResponse, "description": "Internal server error"},
    },
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail={
                "error": 409,
                "message": f"User already exists with email {user.email}"
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
    return user
