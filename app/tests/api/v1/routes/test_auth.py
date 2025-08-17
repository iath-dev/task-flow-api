from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def create_user(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={"email": "testlogin@example.com", "password": "Password123!", "full_name": "Test User"},
    )

def test_signup(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "Password123!", "full_name": "Test User"},
    )
    assert response.status_code == 202
    assert response.json()["message"] == "User registered successfully"
    assert "user" in response.json()


def test_login(client: TestClient, create_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testlogin@example.com", "password": "Password123!"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"