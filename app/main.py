import asyncio

from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager

from app.core.auth import get_current_user
from app.core.db import create_tables, shutdown_engine
from app.core.seeds import run_seeds
from app.routers.notification import router as notifications_router
from app.routers.template import router as template_router
from app.workers.consumer import main as start_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await run_seeds()

    ## worker is running alongside the API,
    # so we use create_task to run it in the background
    # otherwise the worker would need to be deployed separately, which is not the goal of this project
    consumer_task = asyncio.create_task(start_consumer())

    yield

    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass  # noqa: S7497 - Expected cancellation during shutdown

    await shutdown_engine()


app = FastAPI(lifespan=lifespan, dependencies=[Depends(get_current_user)])


app.include_router(
    prefix="/notifications", router=notifications_router, tags=["notifications"]
)

app.include_router(prefix="/template", router=template_router, tags=["templates"])
