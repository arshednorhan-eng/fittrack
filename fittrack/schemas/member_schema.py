from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from fittrack.schemas.validators import PHONE_REGEX, EMAIL_REGEX, ID_REGEX, PASSWORD_REGEX
import re


class MemberCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str
    national_id: str  # 9 digits
    password: str     # strong password

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: EmailStr):
        if not re.fullmatch(EMAIL_REGEX, str(v)):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: str):
        if not re.fullmatch(PHONE_REGEX, v):
            raise ValueError("Invalid phone number format")
        return v

    @field_validator("national_id")
    @classmethod
    def id_valid(cls, v: str):
        if not re.fullmatch(ID_REGEX, v):
            raise ValueError("Invalid national id (must be 9 digits)")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v: str):
        if not re.fullmatch(PASSWORD_REGEX, v):
            raise ValueError("Weak password (min 8, upper+lower+digit+[@#$!])")
        return v


class MemberUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    phone: str | None = None
    status: str | None = None  # validated in model setter (encapsulation)

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: str | None):
        if v is None:
            return v
        if not re.fullmatch(PHONE_REGEX, v):
            raise ValueError("Invalid phone number format")
        return v


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: str
    national_id: str
    status: str
    created_at: datetime
