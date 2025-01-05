from datetime import datetime, timezone
from uuid import UUID
from typing import TYPE_CHECKING

from database import Base

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from auth.models import User


class Messanger(Base):
    __tablename__ = 'messanger'

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), index=True)
    recipient_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), index=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc))
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id], back_populates='message_sender')
    recipient: Mapped['User'] = relationship(foreign_keys=[recipient_id], back_populates='message_recipient')
