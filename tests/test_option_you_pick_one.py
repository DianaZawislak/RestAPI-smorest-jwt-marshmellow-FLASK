"""Tests for new blueprint (beer)"""
import uuid
from pprint import pprint
from tests.test_geography_examples import create_token


# pylint: disable=unused-import
# pylint: disable=consider-using-f-string, no-member, undefined-variable
# pylint: disable=wrong-import-order, no-value-for-parameter, unused-argument

DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
BREWERIES_URL = '/brewery/'
BEERS_URL = '/beers/'
AUTH_URL = '/auth/'


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
