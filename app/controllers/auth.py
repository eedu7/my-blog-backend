from typing import Tuple

from pydantic import EmailStr

from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from app.schemas.responses.users import UserResponse
from core.config import config
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, email: EmailStr, password: str, username: str) -> User:
        # Check if user exists with email
        user = await self.user_repository.get_by_email(str(email))

        if user:
            raise BadRequestException("User already exists with this email")

        # Check if user exists with username
        user = await self.user_repository.get_by_username(username)

        if user:
            raise BadRequestException("User already exists with this username")

        password = PasswordHandler.hash(password)

        return await self.user_repository.create(
            {
                "email": email,
                "password": password,
                "username": username,
            }
        )

    async def login(self, email: EmailStr, password: str) -> Tuple[Token, UserResponse]:
        user = await self.user_repository.get_by_email(str(email))

        if not user:
            raise BadRequestException("Invalid credentials")

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user.id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
            expiry_minutes=config.JWT_EXPIRE_MINUTES
        ), UserResponse(**user.__dict__)

    async def refresh_token(self, refresh_token: str) -> Token:
        token = JWTHandler.decode(refresh_token)
        if token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(
                payload={"sub": "refresh_token", "user_id": token.get("user_id")}
            ),
            expiry_minutes=config.JWT_EXPIRE_MINUTES * 60,  # Convert into seconds
        )
