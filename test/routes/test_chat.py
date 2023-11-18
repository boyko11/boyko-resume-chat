import os

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

os.environ["CHAT_PROVIDER"] = "OpenAIAssistantAPIChatProvider"
os.environ["OPENAI_API_KEY"] = "{your_OPENAI_API_KEY}"


def test_query_endpoint():
    response = client.post("/query", json={"message": "What is Boyko's degree in?", "chat_id": None})
    assert response.status_code == 200
    assert response.json()['message'] != "Hey Sorry, something went wrong with Boyko's resume assistant. " \
                                         "I guess you'd just have to hire him to get to know him better."
    assert response.json()['chat_id'] is not None

    assert "Computer Science" in response.json()['message']
