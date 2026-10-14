
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_create_message():
    response = client.post(
        "/api/v1/messages",
        json={"role": "user", "content": "Hello"}
    )
    assert response.status_code == 201
    assert response.json()["content"] == "Hello"
    assert response.json()["role"] == "user"


def test_list_messages():
    response = client.get("/api/v1/messages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_message_not_found():
    response = client.get("/api/v1/messages/999999")
    assert response.status_code == 404


def test_create_message_invalid_role():
    response = client.post(
        "/api/v1/messages",
        json={"role": "admin", "content": "Hello"}
    )
    assert response.status_code == 422


def test_create_message_empty_content():
    response = client.post(
        "/api/v1/messages",
        json={"role": "user", "content": "   "}
    )
    assert response.status_code == 422


def test_update_message():
    created = client.post(
        "/api/v1/messages",
        json={"role": "user", "content": "Original"}
    )
    message_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/messages/{message_id}",
        json={"content": "Updated"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Updated"


def test_delete_message():
    created = client.post(
        "/api/v1/messages",
        json={"role": "user", "content": "Delete me"}
    )
    message_id = created.json()["id"]

    response = client.delete(f"/api/v1/messages/{message_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/messages/{message_id}")
    assert response.status_code == 404
