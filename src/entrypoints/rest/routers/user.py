"""User Router Module."""

import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status

from src.entrypoints.rest.schemas.shared import ErrorResponseSchema
from src.entrypoints.rest.schemas.user import CreateUserRequest
from src.entrypoints.rest.schemas.user import CreateUserResponse
from src.entrypoints.rest.schemas.user import GetUsersResponse
from src.services.ai_service import AIService
from src.user.repository import BeanieUserRepository
from src.user.service import UserService

# router definition
router = APIRouter(prefix="/user", tags=["User"])


def user_service_factory() -> UserService:
    """User service factory."""
    return UserService(repository=BeanieUserRepository())


def ai_service_factory() -> AIService:
    """AI service factory."""
    return AIService()


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
    ai_service: AIService = Depends(ai_service_factory),
) -> GetUsersResponse:
    """Retrieve a list of users using skip and limit parameters.

    This endpoint delegates the data retrieval to the AI service, which uses an
    AI agent and MCP tools to obtain the list of users. Response validation is
    handled through the GetUsersResponse model.

    Args:
        skip (int | None): Number of records to skip. Must be >= 0.
        limit (int | None): Maximum number of records to return. Must be between 1 and 200.
        ai_service (AIService): Dependency-injected service responsible for interacting with the AI agent.

    Returns:
        GetUsersResponse: The validated list of users returned by the AI service.
    """
    agent = await ai_service.get_ai_agent()

    prompt = (
        "Ottieni la lista utenti.\n"
        "Questi sono i parametri da usare nella chiamata:\n"
        f"- skip: {skip}\n"
        f"- limit: {limit}\n\n"
        "Restituisci **solo** il JSON grezzo che ritorna il tool senza aggiungere altro"
    )

    result = await agent.a_run(prompt)
    text_result = result.text
    if text_result.startswith("```"):
        lines = text_result.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text_result = "\n".join(lines).strip()

        data = json.loads(text_result)

        return GetUsersResponse(**data)
    return text_result


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
