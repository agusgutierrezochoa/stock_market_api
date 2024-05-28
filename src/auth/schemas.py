from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        extra = "forbid"


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    api_key: str

    class Config:
        orm_mode = True


class HTTPErrorResponse(BaseModel):
    error: int
    message: str
