import os


class ChatProviderConfig:
    CHAT_PROVIDER = os.getenv("CHAT_PROVIDER", "OpenAIAssistantAPIChatProvider")
