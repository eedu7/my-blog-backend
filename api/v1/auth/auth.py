
from fastapi import APIRouter, Depends

from app.controllers import AuthController
from app.schemas.extras.token import Token, RefreshTokenRequest
from app.schemas.requests.auth import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory

auth_routers = APIRouter()


@auth_routers.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@auth_routers.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )

@auth_routers.post("/refresh-token")
async def refresh_token(refresh_token_request: RefreshTokenRequest, auth_controller: AuthController = Depends(Factory().get_auth_controller)) -> Token:
    return await auth_controller.refresh_token(**refresh_token_request.model_dump())