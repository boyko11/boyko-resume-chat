from config.config import ChatProviderConfig
from services.chat.chat_provider_anthropic import AnthropicChatProvider
from services.chat.chat_provider_openai_assistant import OpenAIAssistantAPIChatProvider


def get_chat_provider():
    if ChatProviderConfig.CHAT_PROVIDER == "OpenAIAssistantAPIChatProvider":
        return OpenAIAssistantAPIChatProvider()
    elif ChatProviderConfig.CHAT_PROVIDER == "AnthropicChatProvider":
        return AnthropicChatProvider()
    #    Add more conditions here for different providers

    raise ValueError(f"Unknown chat provider: {ChatProviderConfig.CHAT_PROVIDER}")
