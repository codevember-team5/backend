"""User Router Module."""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status

from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.entrypoints.rest.schemas.user import CreateUserRequest
from src.entrypoints.rest.schemas.user import CreateUserResponse
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


@router.post(
    "/",
    summary="Create User",
    response_model=CreateUserResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "User created successfully",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
async def create_user(
    user: CreateUserRequest,
    user_service: UserService = Depends(user_service_factory),
) -> CreateUserResponse:
    """Create User."""
    user = await user_service.create_user(user.fullname)
    return CreateUserResponse(user=user)


@router.delete(
    "/{user_id}",
    summary="Delete User by id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted successfully",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
    },
)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(user_service_factory),
) -> None:
    """Delete User."""
    return await user_service.delete_user(user_id)


@router.post(
    "/assign/{user_id}/device/{device_id}",
    summary="Assign Device to User",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_200_OK: {
            "description": "Device assigned to User successfully",
        },
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema, "description": "Invalid input data"},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema, "description": "Device already assigned to a User"},
    },
)
async def assign_device_to_user(
    user_id: str,
    device_id: str,
    user_service: UserService = Depends(user_service_factory),
) -> None:
    """Assign Device to User."""
    return await user_service.assign_device_to_user(user_id, device_id)
