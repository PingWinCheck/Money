from uuid import uuid4, UUID
from datetime import datetime
from typing import TYPE_CHECKING
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from catalog.models import MoneyForUser
from database import Base


if TYPE_CHECKING:
    from catalog.models import Money


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    update_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    moneys: Mapped[list["Money"]] = relationship('Money', secondary='money_for_users', back_populates='users')

