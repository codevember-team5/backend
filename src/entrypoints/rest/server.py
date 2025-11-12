import time
from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, APIRouter
from starlette.requests import Request
from starlette.responses import Response

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


# middleware
@app.middleware("http")
async def middleware(request: Request, call_next) -> Response:  # noqa: ANN001
    """Middleware.

    Args:
        request (Request): request to be processed
        call_next (Any): callable to forward the request to the right router

    Returns:
        Response: response to be returned to the user
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.debug(f"Request: {request.url.path} process time: {process_time}")
    return response



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
