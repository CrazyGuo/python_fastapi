from typing import Optional
from pydantic import BaseModel, EmailStr


# Shared properties
class UserBaseModelParam(BaseModel):
    email: Optional[EmailStr] = None
    is_available: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserInDBBaseModelParam(UserBaseModelParam):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class UserModelParam(UserInDBBaseModelParam):
    pass

# Properties to receive via API on creation
class UserCreateModelParam(UserBaseModelParam):
    full_name: str
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdateModelParam(UserBaseModelParam):
    password: Optional[str] = None

