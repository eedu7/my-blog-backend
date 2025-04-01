from pydantic import UUID4, BaseModel, Field


class UserResponse(BaseModel):
    email: str = Field(..., examples=["john.doe@example.com"])
    username: str = Field(..., examples=["john.doe"])
    uuid: UUID4 = Field(..., examples=["a3b8f042-1e16-4f0a-a8f0-421e16df0a2f"])

    class Config:
        form_attributes = True
