from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field("bearer", description="Token Type")
    expiry_minutes: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str
