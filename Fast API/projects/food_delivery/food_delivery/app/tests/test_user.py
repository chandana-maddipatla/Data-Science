from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post("/api/v1/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "phone": "9999999999",
        "address": "Test Address"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email():
    client.post("/api/v1/users/register", json={
        "name": "Test User",
        "email": "dup@example.com",
        "password": "testpassword"
    })
    response = client.post("/api/v1/users/register", json={
        "name": "Test User 2",
        "email": "dup@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400


def test_get_user_not_found():
    response = client.get("/api/v1/users/9999")
    assert response.status_code in [401, 404]
