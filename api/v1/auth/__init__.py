from fastapi import APIRouter

from .auth import auth_routers

auth_router = APIRouter()
auth_router.include_router(auth_routers, tags=["Authentication"])

__all__ = ["auth_router"]
