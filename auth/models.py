from uuid import uuid4, UUID
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import func, Enum as PostgresEnum
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
# from catalog.models import MoneyForUser
from database import Base
from enum import Enum


if TYPE_CHECKING:
    from catalog.models import Money


class UserRole(Enum):
    user = 'user'
    admin = 'admin'
    moderator = 'moderator'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str]
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(PostgresEnum(UserRole), default=UserRole.user)
    is_verification_email: Mapped[bool] = mapped_column(default=False, server_default=expression.false())
    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())
    update_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp(),
                                                server_onupdate=func.current_timestamp())
    # update_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
    #                           onupdate=datetime.now(timezone.utc))
    moneys: Mapped[list["Money"]] = relationship('Money', secondary='money_for_users', back_populates='users')
