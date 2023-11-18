from abc import ABC, abstractmethod


class ChatProvider(ABC):

    @abstractmethod
    def chat(self, query: str, chat_id: str | None) -> str:
        """
        Abstract method to send a query and get a response.

        :param query: The user's query as a string.
        :param chat_id: None for th first message in the chat, the chat_id for all messages that follow in this chat
        :return: The response to the query as a string.
        """
        pass
