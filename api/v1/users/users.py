from typing import Callable, Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.controllers import UserController
from app.models.user import User, UserPermission
from app.schemas.responses.users import UserResponse
from core.exceptions import BadRequestException, NotFoundException
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

@user_router.get("/exist/")
async def user_exist(username: Annotated[str | None, Query(min_length=3, max_length=12)] = None,
                     email: Annotated[str | None, Query()] = None,
                     user_controller: UserController = Depends(Factory().get_user_controller)):
    if not username and not email:
        raise BadRequestException("At least specify one `Query` parameter")
    
    user = None
    if username:
        user = await user_controller.get_by_username(username)
    elif email:
        user = await user_controller.get_by_email(email)
    
    if user:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "User found",
                "exist": True,
            }
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User not found",
            "exist": False
        }
    )
    

@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user
