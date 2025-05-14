from pydantic import BaseModel, Field, EmailStr, field_validator
from ..models.user_models import UserRoles
from string import punctuation


def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 digits!")

    contains_lower = False
    contains_upper = False
    contains_special = False
    contains_int = False

    for i in password:
        if i.islower():
            contains_lower = True
        if i.isupper():
            contains_upper = True
        if i in punctuation:
            contains_special = True
        if i.isdigit():
            contains_int = True
    if not (contains_int and contains_lower and contains_upper and contains_special):
        raise ValueError(
            "Password must contain at least one Upper, Lower and special character as well as a number!")

    return password


class UserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: UserRoles = Field(default="User")

    @field_validator("password")
    @classmethod
    def valid_password(cls, password: str) -> str:
        return validate_password(password)


class ShowUserSchema(BaseModel):
    username: str
    email: EmailStr
    role: UserRoles


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    @field_validator("password")
    @classmethod
    def valid_password(cls, password: str) -> str:
        return validate_password(password)
