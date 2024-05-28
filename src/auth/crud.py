from sqlalchemy.orm import Session
import uuid
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    api_key = str(uuid.uuid4())
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        api_key=api_key
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
