"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name, no-member

import pytest
from app import create_app, db
from app.db.models import User


@pytest.fixture()
def application():
    """This makes the app"""
    application = create_app()
    application.config.update({
        "TESTING": True,
    })
    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application  # Note that we changed return for yield, see below for why


@pytest.fixture()
def create_user(application):
    """this creates user"""
    with application.app_context():
        user = User(username="testUser", password="test")
        db.session.add(user)
        db.session.commit()


@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()

@pytest.fixture()
def created_beer_id(client):
    response = client.post(
        "/beers",
        json={"name": "Test beer"},
    )

    return response.json["id"]

@pytest.fixture()
def created_city_id(client):
    response = client.post(
        "/cities",
        json={"name": "Test city"},
    )

    return response.json["id"]


@pytest.fixture()
def created_country_id(client):
    response = client.post(
        "/countries",
        json={"name": "Test country"},
    )

    return response.json["id"]


@pytest.fixture()
def created_brewery_id(client):
    response = client.post(
        "/brewery",
        json={"name": "Test brewery"},
    )

    return response.json["id"]