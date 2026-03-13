from typing import Annotated
import asyncio
import uuid

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from contextlib import asynccontextmanager
from .database import init_db, async_session_maker, GetSession
from .models import UserDB
from .schemas import User, UserCreate, UserUpdate


async def bootstrap_database() -> None:
    await init_db()
    async with async_session_maker() as db:
        result = await db.exec(select(UserDB).where(UserDB.email == "caja"))
        if not result.first():
            db.add(
                UserDB(
                    id=uuid.UUID("2734e76d-de18-4930-8531-54c39b3abe05"),
                    name="caja",
                    email="caja",
                    age=30,
                    password="caja",
                )
            )
            await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bootstrap_database()
    yield

app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

asyncio.run(bootstrap_database())


@app.post("/token", status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: GetSession
):
    result = await db.exec(select(UserDB).where(UserDB.email == form_data.username))
    user = result.first()
    if user and user.password == form_data.password:
        return {"access_token": user.email, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@app.get("/", status_code=status.HTTP_200_OK)
def get_hello():
    return {"message": "Correctly initialized!"}


async def get_user_db(db: GetSession, token: str = Depends(oauth2_scheme)):
    result = await db.exec(select(UserDB).where(UserDB.email == token))
    user = result.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user


@app.get("/me", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(current_user: Annotated[UserDB, Depends(get_user_db)]):
    return current_user


@app.get("/users", status_code=status.HTTP_200_OK, response_model=User)
async def get_users(email: str, db: GetSession):
    result = await db.exec(select(UserDB).where(UserDB.email == email))
    user = result.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UserCreate, db: GetSession):
    result = await db.exec(select(UserDB).where(UserDB.email == user.email))
    if result.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    db_user = UserDB(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        password=user.password,
    )
    db.add(db_user)
    await db.commit()
    return db_user


@app.put("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: uuid.UUID, user: UserUpdate, db: GetSession):
    result = await db.exec(select(UserDB).where(UserDB.id == user_id))
    existing_user = result.first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing_user.id = user.id
    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age
    existing_user.password = user.password

    db.add(existing_user)
    await db.commit()
    return existing_user


@app.patch("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def patch_user(user_id: uuid.UUID, age: int, db: GetSession):
    result = await db.exec(select(UserDB).where(UserDB.id == user_id))
    existing_user = result.first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing_user.age = age
    db.add(existing_user)
    await db.commit()
    return existing_user


@app.delete("/user/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: uuid.UUID, db: GetSession):
    result = await db.exec(select(UserDB).where(UserDB.id == user_id))
    existing_user = result.first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await db.delete(existing_user)
    await db.commit()
    return {"message": "User deleted"}
