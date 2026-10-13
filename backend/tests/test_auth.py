
from datetime import datetime, timedelta, timezone

import jwt

from backend.core.settings import settings


def register_user(client):
    return client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )


def login_user(client):
    return client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
    )


def test_register_user(client):
    response = register_user(client)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "password_hash" not in data


def test_duplicate_email(client):
    first_response = register_user(client)
    second_response = register_user(client)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_success(client):
    register_response = register_user(client)
    assert register_response.status_code == 201

    response = login_user(client)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_wrong_password(client):
    register_user(client)

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_me_with_valid_token(client):
    register_user(client)
    login_response = login_user(client)
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "password_hash" not in response.json()


def test_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer fake.invalid.token"}
    )

    assert response.status_code == 401


def test_me_with_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
