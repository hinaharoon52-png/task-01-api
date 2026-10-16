
from fastapi.testclient import TestClient

from api.main import app

from types import SimpleNamespace
from unittest.mock import patch


from unittest.mock import Mock
from google.genai import errors





client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={"message": "   "},
    )

    assert response.status_code == 422


def test_oversized_message_is_rejected():
    response = client.post(
        "/api/v1/chat",
        json={"message": "a" * 4001},
    )

    assert response.status_code == 422


def test_chat_success():
    fake_result = SimpleNamespace(
        answer="AI is a field of computer science.",
        model="fake-model",
        input_tokens=8,
        output_tokens=9,
    )

    with patch(
        "api.main.generate_reply",
        return_value=fake_result,
    ) as mock_generate:
        response = client.post(
            "/api/v1/chat",
            json={"message": "What is AI?"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "AI is a field of computer science.",
        "model": "fake-model",
        "usage": {
            "input_tokens": 8,
            "output_tokens": 9,
        },
    }
    mock_generate.assert_called_once_with("What is AI?")


def test_chat_timeout():
    with patch(
        "api.main.generate_reply",
        side_effect=TimeoutError(),
    ):
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )

    assert response.status_code == 504
    assert response.json()["detail"] == "LLM provider request timed out."


def test_chat_rate_limit():
    fake_error = errors.APIError.__new__(errors.APIError)
    fake_error.code = 429

    with patch(
        "api.main.generate_reply",
        side_effect=fake_error,
    ):
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )

    assert response.status_code == 429
    assert response.json()["detail"] == (
        "LLM provider rate limit reached. Try again later."
    )


def test_chat_authentication_error():
    fake_error = errors.APIError.__new__(errors.APIError)
    fake_error.code = 403

    with patch(
        "api.main.generate_reply",
        side_effect=fake_error,
    ):
        response = client.post(
            "/api/v1/chat",
            json={"message": "Explain machine learning."},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "LLM provider authentication failed."
    )




