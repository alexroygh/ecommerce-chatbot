import json


def test_chat_message(client):
    # Register and login to get JWT
    client.post(
        "/api/auth/register", json={"username": "chatuser", "password": "test123"}
    )
    login_resp = client.post(
        "/api/auth/login", json={"username": "chatuser", "password": "test123"}
    )
    token = login_resp.get_json().get("access_token")
    assert token

    # Send a chat message
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/chat", json={"message": "Hello!"}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data
