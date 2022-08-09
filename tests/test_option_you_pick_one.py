"""Tests for new blueprint (beer)"""
# pylint: disable=unused-import
import uuid
from pprint import pprint
from flask_jwt_extended import create_access_token, decode_token
from app import db, app, config
from app.db.models import  User, Beer, Brewery


DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
BREWERIES_URL = '/brewery/'
BEERS_URL = '/beers/'
AUTH_URL = '/auth/'

# pylint: disable=consider-using-f-string, no-member, undefined-variable
# pylint: disable=wrong-import-order, no-value-for-parameter, unused-argument
from tests.test_geography_examples import create_token



def test_create_beer_brewery(application):
    """test create city-country"""
    with application.app_context():
        brewery = Brewery(name="18th Street Brewery")
        db.session.add(brewery)
        db.session.commit()
        beer = Beer(name="Devil's Cup", brewery_id=brewery.id)
        db.session.add(beer)
        db.session.commit()

        assert beer.brewery.name == "18th Street Brewery"

def test_brewery_post(client, create_user):
    """test post country"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "18th Street Brewery"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/brewery', json=data, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data["name"] == "18th Street Brewery"

def test_beer_post(client, create_user):
    """test post beer"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "18th Street Brewery"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/brewery', json=data, headers=headers)
    response_data = response.get_json()
    brewery_id = response_data['id']
    pprint(brewery_id)

    data = {"brewery_id": brewery_id, "name": "Devil's Cup"}

    response = client.post('/beers', json=data, headers=headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Devil's Cup"


def test_beer_delet(client, create_user):
    """test post beer"""
    with client.application.app_context():
        access_token = create_token()

    data = {"name": "18th Street Brewery"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.delete('/brewery', json=data, headers=headers)
    response_data = response.get_json()
    brewery_id = response_data['id']
    pprint(brewery_id)

    data = {"brewery_id": brewery_id, "name": "Devil's Cup"}

    response = client.post('/beers', json=data, headers=headers)
    assert response.status_code == 204
    #response_data = response.get_json()
    #assert response_data["id"] == 1
    #assert response_data["name"] == "Devil's Cup"