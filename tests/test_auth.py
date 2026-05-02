from datetime import timedelta
from app.core.jwt import create_access_token

def test_signup_success(client):
    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "secret123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_signup_duplicate_email(client):
    client.post(
        "/api/v1/users/signup",
        json={
            "email": "duplicate@example.com",
            "name": "Duplicate",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "duplicate@example.com",
            "name": "Duplicate",
            "password": "secret123"
        }
    )

    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/users/signup",
        json={
            "email": "login@example.com",
            "name": "Login User",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "login@example.com",
            "name": "Login User",
            "password": "secret123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/api/v1/users/signup",
        json={
            "email": "wrong@example.com",
            "name": "Wrong User",
            "password": "secret123"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "wrong@example.com",
            "name": "Wrong User",
            "password": "badpassword"
        }
    )

    assert response.status_code == 401


def test_get_me_requires_token(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code in [401, 403]


def test_get_me_success(client, auth_headers):
    response = client.get(
        "/api/v1/users/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "auth@example.com"
    assert data["name"] == "Auth User"
    assert "id" in data

def test_get_me_invalid_token(client):
    headers = {
        "Authorization": "Bearer invalidtoken123"
    }

    response = client.get(
        "/api/v1/users/me",
        headers=headers
    )

    assert response.status_code == 401


def test_get_me_expired_token(client):
    # create user
    signup_response = client.post(
        "/api/v1/users/signup",
        json={
            "email": "expired@example.com",
            "name": "Expired User",
            "password": "secret123"
        }
    )

    user_id = signup_response.json()["id"]

    # create expired token using real user id
    expired_token = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(seconds=-10)
    )

    headers = {
        "Authorization": f"Bearer {expired_token}"
    }

    response = client.get(
        "/api/v1/users/me",
        headers=headers
    )

    assert response.status_code == 401

