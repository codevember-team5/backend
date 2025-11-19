"""REST API server."""

import json
import time

from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response

from src.common.exceptions import InvalidArgumentError
from src.common.exceptions import NotDeletableError
from src.common.exceptions import NotFoundError
from src.common.exceptions import NotUpdatableError
from src.database import database
from src.entrypoints.rest.routers import historical
from src.entrypoints.rest.routers import user
from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.mcp_server.mcp_server import mcp
from src.settings import get_logger
from src.settings import settings

# logger
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the lifespan."""
    client = database.get_db_connection()
    await database.init_db(client)
    app.state.mongo_client = client

    async with mcp_app.lifespan(app):
        try:
            yield
        finally:
            await app.state.mongo_client.close()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
)
# base router
base_router = APIRouter(prefix="/api")
base_router.include_router(user.router)
base_router.include_router(historical.router)
# register routers
app.include_router(base_router)

# mount MCP app
mcp_app = mcp.http_app(path="/")
app.mount("/mcp", mcp_app)


# error handling
@app.exception_handler(Exception)
async def exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Exception handler.

    Args:
        _ (Request): http Request
        exc (Exception): exception

    Returns:
        JSONResponse: JSON response with error details
    """
    res = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "details": type(exc).__name__,
        },
    )
    if isinstance(exc, NotFoundError):
        res = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )
    if isinstance(exc, NotDeletableError | NotUpdatableError):
        res = JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )
    if isinstance(
        exc,
        InvalidArgumentError | ValueError,
    ):
        res = JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )
    return res


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
