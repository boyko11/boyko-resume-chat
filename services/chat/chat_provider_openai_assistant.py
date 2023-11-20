import os
import re
from time import sleep

from openai import OpenAI, NotFoundError

from config.config import AssistantConfig, PersonConfig
from config.logger_config import logger
from models.chat.chat_message import ChatMessage
from services.chat.chat_provider_abstract import ChatProvider


class OpenAIAssistantAPIChatProvider(ChatProvider):

    _assistant = None

    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        OpenAIAssistantAPIChatProvider._assistant = self._get_assistant()

    def chat(self, query: str, chat_id: str | None) -> ChatMessage:

        # Create a thread if first time interaction
        if not chat_id:
            thread = self.client.beta.threads.create()
            logger.info(f"Created thread: {thread.id}")
        else:
            thread = self.client.beta.threads.retrieve(chat_id)
            logger.info(f"Retrieved thread: {thread.id}")

        # Create a message
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        # Create and run the interaction
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=OpenAIAssistantAPIChatProvider._assistant.id
        )

        # Wait for the run to complete
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        logger.info(f"Waiting for Message from Assistant: {thread.id}. run.status: {run.status}")
        while run.status in ['in_progress', 'queued']:
            sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            logger.info(f'run.status: {run.status}')

        # Check if the run was successful and create ChatMessage instance
        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            assistant_message = list(messages)[0].content[0].text.value
            assistant_message = self._remove_citations(assistant_message)
            return ChatMessage(message=assistant_message, chat_id=thread.id)
        elif run.status == 'failed':
            return ChatMessage(
                message=f"Run failed: code: {run.last_error.code}, message: {run.last_error.message}",
                chat_id=thread.id
            )

        return ChatMessage(
            message=f"Hey Sorry, something went wrong with {PersonConfig.name}'s resume assistant. " \
                    "I guess you'd just have to hire him to get to know him better.",
            chat_id=thread.id
        )

    def _get_assistant(self):
        """Look for the existing assistant. If one does not exist, create a new one"""
        if OpenAIAssistantAPIChatProvider._assistant:
            return OpenAIAssistantAPIChatProvider._assistant

        # local import because of circular import
        from main import BASE_DIR

        assistant_id_file_path = os.path.join(BASE_DIR, 'config/assistant_id.txt')

        if os.path.exists(assistant_id_file_path):

            with open(assistant_id_file_path, "r") as assistant_id_file:
                assistant_id = assistant_id_file.read()
            try:
                return self.client.beta.assistants.retrieve(assistant_id)
            except NotFoundError:
                logger.warn(f"No assistant found for {assistant_id}. Creating new assistant...")

        else:
            logger.warn("assistant_id.txt file not found. Creating new assistant...")

        resume_file = self.client.files.create(
            file=open(os.path.join(BASE_DIR, 'config/data/Resume.txt'), "rb"),
            purpose='assistants'
        )

        # Create an assistant
        assistant = self.client.beta.assistants.create(
            name=AssistantConfig.name,
            description=AssistantConfig.description,
            instructions=AssistantConfig.instructions,
            tools=[{"type": "retrieval"}],
            model=AssistantConfig.model,
            file_ids=[resume_file.id]
        )

        with open(os.path.join(BASE_DIR, 'config/assistant_id.txt'), "w") as assistant_id_file:
            assistant_id_file.write(assistant.id)

        logger.info(f'Created assistant {assistant.id}')
        return assistant

    @staticmethod
    def _remove_citations(text: str) -> str:
        citation_pattern = "【\\d+†source】"
        clean_text = re.sub(citation_pattern, '', text)
        return clean_text.strip()

