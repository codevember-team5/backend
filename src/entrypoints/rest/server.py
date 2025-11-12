from fastapi import FastAPI, APIRouter

from src.entrypoints.rest.routers import user

app = FastAPI(
    docs_url="/api/docs",
)
base_router = APIRouter(prefix="/api")
base_router.include_router(user.router)
# register routers
app.include_router(base_router)