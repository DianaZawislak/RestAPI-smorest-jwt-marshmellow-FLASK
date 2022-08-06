"""these are tests for brewery/beer  and some country/city API endpoints"""
# pylint: disable=unused-import
from pprint import pprint
from flask_jwt_extended import create_access_token, decode_token
from app import db, app, config
from app.db.models import City, Country, User, Beer, Brewery


# pylint: disable=consider-using-f-string, no-member, undefined-variable
# pylint: disable=wrong-import-order, no-value-for-parameter, unused-argument


def test_delete_city(client, created_city_id):
    """this tests city delete method"""
    response = client.delete(
        f"/cities/{created_city_id}",
    )

    assert response.status_code == 200
    assert response.json["message"] == "City deleted"


def test_get_city_not_found(client):
    """this tests city not found"""
    response = client.get(
        "/cities/1999",
    )

    assert response.status_code == 404
    assert response.json == {"code": 404, "status": "Not Found"}


def test_post_country_without_admin(client, jwt, created_country_id):
    """this tests post country without authorization"""
    response = client.post(
        f"/countries/{created_country_id}",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"


def test_post_city_without_admin(client, jwt, created_city_id):
    """this tests post city without authorization"""
    response = client.post(
        f"/cities/{created_city_id}",
        headers={"Authorization": f"Bearer {jwt}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "Missing Authorization Header"


def create_token():
    """this tests create token"""
    user = User.query.first()
    access_token = create_access_token(user.username)
    return access_token
