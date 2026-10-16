
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_llm_service
from app.core.exceptions import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMUnavailableError,
)


class FakeLLMService:
    """Fake LLM service for tests without calling Gemini."""

    def __init__(self, error=None):
        self.error = error

    async def generate_reply(self, message: str):
        if self.error is not None:
            raise self.error

        return SimpleNamespace(
            answer="AI is a field of computer science.",
            model="fake-model",
            input_tokens=8,
            output_tokens=9,
        )


client = TestClient(app)


def setup_fake_service(error=None):
    app.dependency_overrides[get_llm_service] = (
        lambda: FakeLLMService(error=error)
    )


def teardown_fake_service():
    app.dependency_overrides.clear()


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Chat API is running"


def test_empty_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={"message": "   "},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_oversized_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={"message": "a" * 4001},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_chat_success():
    setup_fake_service()

    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "What is AI?"},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 200
    assert response.json() == {
        "answer": "AI is a field of computer science.",
        "model": "fake-model",
        "usage": {
            "input_tokens": 8,
            "output_tokens": 9,
        },
    }


def test_custom_request_id_is_preserved():
    setup_fake_service()

    try:
        response = client.post(
            "/api/v1/chat",
            headers={"X-Request-ID": "task04-test-123"},
            json={"message": "What is AI?"},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "task04-test-123"


def test_request_id_is_generated_when_missing():
    setup_fake_service()

    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "What is AI?"},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 200
    assert response.headers.get("x-request-id")


def test_unavailable_error_returns_safe_503():
    setup_fake_service(LLMUnavailableError())

    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "llm_unavailable"
    assert response.json()["error"]["request_id"]


def test_rate_limit_error_returns_429():
    setup_fake_service(LLMRateLimitError())

    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "llm_rate_limited"


def test_authentication_error_returns_safe_502():
    setup_fake_service(LLMAuthenticationError())

    try:
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )
    finally:
        teardown_fake_service()

    assert response.status_code == 502
    assert response.json()["error"]["code"] == "llm_configuration_error"
    assert "API key" not in response.text
