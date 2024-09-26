from uuid import UUID
from typing import TYPE_CHECKING
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from auth.models import User


class Ruler(Base):
    __tablename__ = 'rulers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    start_year: Mapped[int]
    finish_year: Mapped[int]
    photo_link: Mapped[str | None] = None
    type_moneys: Mapped[list["TypeMoney"]] = relationship('TypeMoney', back_populates='ruler')


class TypeMoney(Base):
    __tablename__ = 'types_moneys'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    photo_link: Mapped[str | None] = None
    ruler_id: Mapped[int] = mapped_column(ForeignKey('rulers.id'))
    ruler: Mapped["Ruler"] = relationship('Ruler', back_populates='type_moneys')
    moneys: Mapped[list["Money"]] = relationship('Money', back_populates='type_money')


class Money(Base):
    __tablename__ = 'moneys'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int]
    photo_link: Mapped[str | None] = None
    type_money_id: Mapped[int] = mapped_column(ForeignKey('types_moneys.id'))
    type_money: Mapped["TypeMoney"] = relationship("TypeMoney", back_populates='moneys')
    users: Mapped[list["User"]] = relationship('User', secondary='money_for_users', back_populates='moneys')


class MoneyForUser(Base):
    __tablename__ = 'money_for_users'

    money_id: Mapped[int] = mapped_column(ForeignKey('moneys.id'), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), primary_key=True)
    # count: Mapped[int] = mapped_column(default=1, server_default='1', )

