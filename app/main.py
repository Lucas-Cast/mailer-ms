from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.core.db import create_tables, shutdown_engine
from app.core.seeds import run_seeds
from app.routers.notification import router as notifications_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await run_seeds()

    yield

    await shutdown_engine()


app = FastAPI(lifespan=lifespan)


app.include_router(
    prefix="/notifications", router=notifications_router, tags=["notifications"]
)
