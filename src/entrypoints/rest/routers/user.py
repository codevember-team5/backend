from fastapi import APIRouter
from pymongo import AsyncMongoClient
from starlette import status

from src.database.database import get_db_connection
from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.entrypoints.rest.schemas.user import GetUsersResponse, User
from src.settings import settings

# router definition
router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/",
    summary="Get Users",
    response_model=GetUsersResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the filtered list of OAs",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
def get_users():
    client = AsyncMongoClient(
        host=settings.db.uri,
    )
    client.get_database(settings.db.dbname)
    print(client.get_database(settings.db.dbname))
    return GetUsersResponse(users=[User(fullname="John Doe", devices=["device1"])])