"""these are tests for brewery/beer  and some country/city API endpoints"""
# pylint: disable=unused-import
from pprint import pprint
from flask_jwt_extended import create_access_token, decode_token
from app import db, app, config
from app.db.models import City, Country, User, Beer, Brewery


# pylint: disable=consider-using-f-string, no-member, undefined-variable
# pylint: disable=wrong-import-order, no-value-for-parameter, unused-argument

def test_create_brewery(application):
    """this tests create the brewery method"""
    with application.app_context():
        brewery = Brewery(name="18th Street Brewery")
        db.session.add(brewery)
        db.session.commit()

        assert brewery.name == "18th Street Brewery"

def test_create_beer(application):
    """this tests create the beer method"""
    with application.app_context():
        brewery = Brewery(name="18th Street Brewery")
        beer = Beer(name="Devil's Cup", brewery_id=brewery.id)
        db.session.add(beer)
        db.session.commit()

        assert beer.name == "Devil's Cup"


def test_brewery_post(client, create_user):
    # pylint: disable=unused-argument
    """this tests country post method"""
    with client.application.app_context():
        access_token = create_token()

    data = {"brewery": "18th Street Brewery"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/beer/breweries', json=data, headers=headers)
    response_data = response.get_json()
    assert response.status_code == 201
    assert response_data["brewery"] == "18th Street Brewery"



def test_beer_post(client, create_user):
    # pylint: disable=unused-argument
    """this tests beer post method"""
    with client.application.app_context():
        access_token = create_token()

    data = {"brewery": "United States"}

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = client.post('/beer/breweries', json=data, headers=headers)
    response_data = response.get_json()
    brewery_id = response_data['brewery_id']
    pprint(brewery_id)

    data = {"brewery_id": brewery_id, "name": "Devil's Cup"}

    response = client.post('/beer/breweries', json=data, headers=headers)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["id"] == 1
    assert response_data["name"] == "Devil's Cup"


def create_token():
    """this tests create token"""
    user = User.query.first()
    access_token = create_access_token(user.username)
    return access_token

def test_countries_route():
    """Testing the routes to list records"""
    response = app.test_client().get('/countries')
    assert response.status_code == 304

def test_city_route():
    """Testing the routes to list records"""
    response = app.test_client().get('/cities')
    assert response.status_code == 304

def test_brewery_route():
    """Testing the routes to list records"""
    response = app.test_client().get('/breweries')
    assert response.status_code == 304

def test_beer_route():
    """Testing the routes to list records"""
    response = app.test_client().get('/beers')
    assert response.status_code == 304
