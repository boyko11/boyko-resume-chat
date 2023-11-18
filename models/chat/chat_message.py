from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str
    chat_id: str | None = None
