"""user tests with token refresh"""
import uuid

import pytest


# pylint: disable=redefined-outer-name, unused-argument


DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
COUNTRIES_URL = '/countries/'
CITIES_URL = '/cities/'
AUTH_URL = '/auth/'


@pytest.fixture()
def created_user_jwts(client, created_user_details):
    """fixture"""
    username, password = created_user_details
    response = client.post(
        "/auth",
        json={"username": username, "password": password},
    )

    return response.json["access_token"]


@pytest.fixture()
def created_user_details(client):
    """fixture"""
    username = "test_user"
    password = "test_password"
    client.post(
        "/register",
        json={"username": username, "password": password},
    )

    return username, password


def test_register_user_already_exists(client):
    """testing user already exists"""
    username = "test_user"
    client.post(
        "/register",
        json={"username": username, "password": "Test Password"},
    )

    response = client.post(
        "/register",
        json={"username": username, "password": "Test Password"},
    )

    assert response.status_code == 200


def test_login_user_bad_password(client, created_user_details):
    """testing wrong password"""
    username, _ = created_user_details
    response = client.post(
        "/auth",
        json={"username": username, "password": "bad_password"},
    )

    assert response.status_code == 401


def test_login_user_bad_username(client, created_user_details):
    """testing wrong user name"""
    _, password = created_user_details
    response = client.post(
        "/auth",
        json={"username": "bad_username", "password": password},
    )

    assert response.status_code == 401


def test_get_user_details(client, create_user):
    """testing get user details"""
    response = client.get(
        "/user_info",
    )

    assert response.status_code == 401


def test_refresh_token(client, create_user):
    """Test refresh token"""
    response = client.post(
        "/auth",
        headers={"Authorization": f"Bearer {created_user_jwts[1]}"},
    )

    assert response.status_code == 200
    assert response.json["access_token"]
