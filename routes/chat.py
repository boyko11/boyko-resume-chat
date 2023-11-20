from fastapi import APIRouter, HTTPException
from services.chat.chat_provider_factory import get_chat_provider
from config.logger_config import logger
from models.chat.chat_message import ChatMessage

chat_router = APIRouter()


@chat_router.post("/query", response_model=ChatMessage)
async def query(chat_message: ChatMessage) -> ChatMessage:
    try:
        query_text = chat_message.message

        if not query_text:
            raise HTTPException(status_code=400, detail="Query text is required")

        logger.info(f"Received query: {query_text}")
        chat_provider = get_chat_provider()
        response = chat_provider.chat(query_text, chat_message.chat_id)
        logger.info(f"Response: {response}")

        return ChatMessage(message=response.message, chat_id=response.chat_id)
    except Exception as e:
        logger.error(f"Error in processing the query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
