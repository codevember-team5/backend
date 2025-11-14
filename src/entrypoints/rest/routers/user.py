"""User Router Module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status

from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.entrypoints.rest.schemas.user import GetUsersResponse
from src.user.repository import BeanieUserRepository
from src.user.service import UserService

# router definition
router = APIRouter(prefix="/user", tags=["User"])


def user_service_factory() -> UserService:
    """User service factory."""
    return UserService(repository=BeanieUserRepository())


@router.get(
    "/",
    summary="Get Users",
    response_model=GetUsersResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Returns the list of Users",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
async def get_users(
    skip: int | None = Query(default=None, ge=0),
    limit: int | None = Query(default=None, ge=1, le=200),
    user_service: UserService = Depends(user_service_factory),
) -> GetUsersResponse:
    """Get Users."""
    users = await user_service.get_users(skip, limit)
    return GetUsersResponse(users=users)
