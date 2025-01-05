from uuid import UUID

from sqlalchemy import select, or_, and_, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.dao import BaseDAO
from chat.models import Messanger


class MessangerDAO(BaseDAO):
    model = Messanger

    @classmethod
    async def send_message(cls, sender_id: UUID, recipient_id: UUID, content: str, session: AsyncSession) -> model:
        new_message = cls.model(sender_id=sender_id, recipient_id=recipient_id, content=content)
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message

    @classmethod
    async def get_messages_p2p(cls,
                               sender_id: UUID,
                               recipient_id: UUID,
                               session: AsyncSession) -> list[model]:
        query = select(cls.model).filter(
            or_(
                and_(cls.model.sender_id == sender_id, cls.model.recipient_id == recipient_id),
                and_(cls.model.sender_id == recipient_id, cls.model.recipient_id == sender_id)
            )
        ).order_by(desc(cls.model.id)).options(joinedload(cls.model.sender)).options(joinedload(cls.model.recipient))
        result = await session.scalars(query)
        return list(result)
