import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    age: int


class UserCreate(UserBase):
    id: uuid.UUID
    password: str


class UserUpdate(UserCreate):
    pass


class User(UserCreate):
    class Config:
        from_attributes = True
