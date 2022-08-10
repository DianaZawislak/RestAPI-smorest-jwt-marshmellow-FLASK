"""these are tests  for  country/city API endpoints"""
# pylint: disable=unused-import
import secrets
import string
import uuid
import datetime as dt
from pprint import pprint
from flask_jwt_extended import create_access_token, decode_token
from app import db, app, config
from app.db.models import City, Country, User, Beer, Brewery
# pylint: disable=invalid-name



DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
COUNTRIES_URL = '/countries/'
CITIES_URL = '/cities/'
AUTH_URL = '/auth/'

# pylint: disable=consider-using-f-string, no-member, undefined-variable
# pylint: disable=wrong-import-order, no-value-for-parameter, unused-argument


def test_get_city_not_found(client):
    """this tests city not found"""
    response = client.get(
        "/cities/1999",
    )

    assert response.status_code == 401


def create_token():
    """this tests create token"""
    user = User.query.first()
    access_token = create_access_token(user.username)
    return access_token


def test_delete_city(client, admin_jwt, created_city_id):
    """test delete city"""
    response = client.delete(
        f"/item/{created_city_id}",
        headers={"Authorization": f"Bearer {admin_jwt}"},
    )

    assert response.status_code == 200


def test_get_country_not_found(client):
    """test country not found"""
    response = client.get(
        "/country/1",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}
