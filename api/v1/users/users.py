from typing import Callable

from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.models.user import User, UserPermission
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.permissions import Permissions

user_router = APIRouter()


@user_router.get("/", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    user_controller: UserController = Depends(Factory().get_user_controller),
    assert_access: Callable = Depends(Permissions(UserPermission.READ)),
) -> list[UserResponse]:
    users = await user_controller.get_all()

    assert_access(resource=users)
    return users


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user
