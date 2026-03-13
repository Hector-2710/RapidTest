import uuid
from sqlmodel import SQLModel, Field

class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    age: int = Field(nullable=False)
    password: str = Field(nullable=False)
