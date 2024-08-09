from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __table_name__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default_factory=func.now)
    update_at: Mapped[datetime] = mapped_column(default_factory=func.now, onupdate=func.now())

