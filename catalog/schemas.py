from typing import Any

from pydantic import BaseModel, ConfigDict
from auth.schemas import UserRead


class RulerSchema(BaseModel):
    id: int
    name: str
    start_year: int
    finish_year: int
    photo_link: str


class TypeMoneySchema(BaseModel):
    id: int
    type_name: str
    photo_link: str
    ruler: RulerSchema


class MoneySchema(BaseModel):
    id: int
    title: str
    year: int
    photo_link: str
    type_money: TypeMoneySchema


class MoneySchemaExcludeYear(BaseModel):
    id: int
    title: str
    photo_link: str
    type_money: TypeMoneySchema


class MoneyFromTheUser(UserRead):
    moneys: list[MoneySchema]


