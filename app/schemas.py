# ------- IMPORTS -------

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr
)

from datetime import datetime

# ------- SCHEMAS -------
class UserBase(BaseModel):
    username: str = Field(min_length = 1, max_length = 30)
    email: EmailStr = Field(max_length = 60)

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    username: str | None = Field(default = None, min_length = 1, max_length = 30)
    email: EmailStr | None = Field(default = None, max_length = 60)

# Eventually will be split into UserPrivate and UserPublic
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes = True)

    id: int
    created_at: datetime