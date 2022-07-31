"""these are tests for country/city API endpoints"""
from pprint import pprint
from app import db
from app.db.models import City, Country, User
from flask_jwt_extended import create_access_token, decode_token

# pylint: disable=consider-using-f-string, no-member, wrong-import-order,
# pylint: disable=unused-import, unused-argument

def test_create_city_country(application):
    """this tests create the city method"""
    with application.app_context():
        country = Country(name="United States")
        db.session.add(country)
        db.session.commit()
        city = City(name="New York", country_id=country.id)
        db.session.add(city)
        db.session.commit()

        assert city.country.name == "United States"


def test_country_post(client, create_user):
    """this tests country post method"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "United States"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/geography/countries', json=data, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data["name"] == "United States"



def test_city__post(client, create_user):
    """this tests city post method"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "United States"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/geography/countries', json=data, headers=headers)
    response_data = response.get_json()
    country_id = response_data['id']
    pprint(country_id)

    data = {"country_id": country_id, "name": "Newark"}

    response = client.post('/geography/cities', json=data, headers=headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Newark"


def create_token():
    """this tests create token"""
    user = User.query.first()
    access_token = create_access_token(user.username)
    return access_token
