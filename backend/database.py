import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


def _load_database_url() -> str | None:
    env_value = os.getenv("DATABASE_URL")
    if env_value:
        return env_value

    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return None

    for line in env_path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#") or "=" not in item:
            continue

        key, value = item.split("=", 1)
        if key.strip() == "DATABASE_URL":
            return value.strip().strip('"').strip("'")

    return None


DATABASE_URL = _load_database_url()

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    poolclass=NullPool,
)

# Create async session factory
async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as eg:
        await eg.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Dependency for getting async database session"""
    async with async_session_maker() as session:
        yield session

GetSession = Annotated[AsyncSession, Depends(get_session)]