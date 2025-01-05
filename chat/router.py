from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from auth.dependences import get_active_current_user
from auth.models import User
from chat.dao import MessangerDAO
from auth.dao import UserDAO
from chat.schemas import MessangerSchema

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/send-message/{recipient_user_id}', response_model=MessangerSchema)
async def send_message(recipient_user_id: UUID,
                       current_user: Annotated[User, Depends(get_active_current_user)],
                       content: Annotated[str, Body()],
                       session: Annotated[AsyncSession, Depends(get_session)]):
    recipient = await UserDAO.get_one_or_none_item_by_id(id_=recipient_user_id, session=session)
    if recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User is not found')
    message = await MessangerDAO.send_message(sender_id=current_user.id,
                                              recipient_id=recipient_user_id,
                                              content=content,
                                              session=session)
    return message


@router.get('/messages/{recipient_user_id}', response_model=Optional[list[MessangerSchema]])
async def messages(recipient_user_id: UUID,
                   current_user: Annotated[User, Depends(get_active_current_user)],
                   session: Annotated[AsyncSession, Depends(get_session)]):
    recipient = await UserDAO.get_one_or_none_item_by_id(id_=recipient_user_id, session=session)
    if recipient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User is not found')
    return await MessangerDAO.get_messages_p2p(sender_id=current_user.id,
                                               recipient_id=recipient_user_id,
                                               session=session)
