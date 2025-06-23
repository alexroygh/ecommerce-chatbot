import json

def test_register_and_login(client):
    # Register a new user
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 201 or response.status_code == 400  # 400 if already exists

    # Login with the new user
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data 