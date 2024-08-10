from pydantic import BaseModel, EmailStr, Field, dataclasses, ConfigDict
from typing import Annotated
from fastapi import Form
from dataclasses import dataclass


@dataclass
class User:
    username: Annotated[str, Form()]
    email: Annotated[EmailStr, Form()]


@dataclass
class UserCreate(User):
    password: Annotated[str, Form()]


class UserCreate1(BaseModel):
    username: str
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)
