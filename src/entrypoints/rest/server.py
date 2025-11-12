from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, APIRouter

from src.database import database
from src.entrypoints.rest.routers import user
from src.settings import get_logger, settings

# logger
logger = get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db(app)
    try:
        yield
    finally:
        await app.state.mongo_client.close()

app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
)
base_router = APIRouter(prefix="/api")
base_router.include_router(user.router)
# register routers
app.include_router(base_router)


# enable remote debugging if DEBUG env variable is set
# to enable debug during development on docker
if settings.debug:
    import debugpy

    logger.debug(json.dumps(settings.model_dump(), indent=2))

    debugpy.listen(("0.0.0.0", 5678))  # noqa S104
    logger.info("debugger listening on container port: 5678")

    if settings.wait_for_debugger_connected:
        logger.info("Waiting for debugger to attach...")
        debugpy.wait_for_client()
        logger.info("Debugger attached. Continuing execution.")
