from pydantic import BaseModel, ConfigDict


class RulerSchema(BaseModel):
    id: int
    name: str
    start_year: int
    finish_year: int
    photo_link: str


class TypeMoneySchema(BaseModel):
    ruler: RulerSchema
    id: int
    type_name: str
    photo_link: str
    ruler_id: int
