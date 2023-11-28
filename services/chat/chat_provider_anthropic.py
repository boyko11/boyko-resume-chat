import os

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from config.config import AssistantConfig
from config.logger_config import logger
from models.chat.chat_message import ChatMessage
from services.chat.chat_provider_abstract import ChatProvider


class AnthropicChatProvider(ChatProvider):
    # local import due to circular dependency
    from main import BASE_DIR
    with open(os.path.join(BASE_DIR, 'config/data/Resume.txt')) as f:
        resume_text = f.read()
        resume_text = "Boyko's resume: \n\n" + resume_text

    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def chat(self, query: str, chat_id: str | None) -> ChatMessage:

        logger.info(f'Query for Claude: {query}')
        prompt = (
            f"{AssistantConfig.instructions}\n\n{AnthropicChatProvider.resume_text}\n\n"   
            f"{HUMAN_PROMPT} {query}{AI_PROMPT}"
        )

        anthropic = Anthropic()
        completion = anthropic.completions.create(
            prompt=prompt,
            max_tokens_to_sample=300,
            model="claude-2"
        )

        response = completion.completion

        logger.info(f"Claude's response: {response}")

        return ChatMessage(message=response)
