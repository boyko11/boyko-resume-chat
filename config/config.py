import os
import json
from typing import TypeVar, Type

from pydantic import BaseModel

# Create a generic type variable for Pydantic models
T = TypeVar('T', bound='BaseModel')


class ChatProviderConfig:
    CHAT_PROVIDER = os.getenv("CHAT_PROVIDER", "OpenAIAssistantAPIChatProvider")


class JsonConfigMixin:
    @classmethod
    def load_config(cls: Type[T], file_path: str) -> None:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for key, value in data.items():
                setattr(cls, key, value)


class AssistantConfig(JsonConfigMixin, BaseModel):
    name: str = None
    description: str = None
    instructions: str = None
    tools: list[dict[str, str]] = None
    model: str = None


AssistantConfig.load_config('config/AssistantConfig.json')


class PersonConfig(JsonConfigMixin, BaseModel):
    name: str = None


PersonConfig.load_config('config/PersonConfig.json')
