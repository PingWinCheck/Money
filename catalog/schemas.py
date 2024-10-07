from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict, Field
from auth.schemas import UserRead


class RulerSchema(BaseModel):
    id: int
    name: Annotated[str, Field(description='Имя правителя')]
    start_year: int
    finish_year: int
    photo_link: str


class RulersResponseSchema(BaseModel):
    total_items: int
    items_per_page: int
    current_page: int
    total_pages: int
    data: list[RulerSchema]


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


