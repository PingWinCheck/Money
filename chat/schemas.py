from uuid import UUID

from pydantic import BaseModel


class SenderSchema(BaseModel):
    username: str


class RecipientSchema(BaseModel):
    username: str


class MessangerSchema(BaseModel):
    sender: SenderSchema
    recipient: RecipientSchema
    content: str
    sender_id: UUID
    recipient_id: UUID
