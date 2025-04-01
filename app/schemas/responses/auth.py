
from pydantic import BaseModel


from app.schemas.extras.token import Token
from app.schemas.responses.users import UserResponse


class AuthResponse(BaseModel):
    message: str
    token: Token
    user: UserResponse

    class Config:
        form_attributes = True