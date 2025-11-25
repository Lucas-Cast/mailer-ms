from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def shutdown_engine():
    await engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_factory() as session:
        yield session
