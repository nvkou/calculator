from fastapi.testclient import TestClient

def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": 'a',
        "email": "fake@q.a",
        "password": "123456",
    }
    r = client.post("http://127.0.0.1:8000/login/", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "token" in tokens
    assert tokens["token"]
