from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_invalid_credentials():
    response = client.post("/api/v1/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_success():
    client.post("/api/v1/users/register", json={
        "name": "Auth User",
        "email": "authuser@example.com",
        "password": "securepass",
        "phone": "9999999999",
        "address": "Hyderabad"
    })
    response = client.post("/api/v1/auth/login", data={
        "username": "authuser@example.com",
        "password": "securepass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()