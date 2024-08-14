from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated
from fastapi import Form
from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    username: Annotated[str, Form()]
    email: Annotated[EmailStr, Form()]


@dataclass
class UserCreate(User):
    password: Annotated[str, Form()]


class UserBase(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

