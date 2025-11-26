from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import env_variables
from app.models import *

engine = create_async_engine(url=env_variables.pg_url)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def shutdown_engine() -> None:
    await engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_factory() as session:
        yield session
