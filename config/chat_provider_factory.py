from config.config import ChatProviderConfig
from services.chat.chat_provider_openai_assistant import OpenAIAssistantAPIChatProvider


def get_chat_provider():
    if ChatProviderConfig.CHAT_PROVIDER == "OpenAIAssistantAPIChatProvider":
        return OpenAIAssistantAPIChatProvider()
    # Add more conditions here for different providers
    # else if CHAT_PROVIDER == "AnotherProvider":
    #     return AnotherProvider()

    raise ValueError(f"Unknown chat provider: {ChatProviderConfig.CHAT_PROVIDER}")
