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

class TestApi:
    """TEST API"""
    jwt_token = None
    brewery_1_id = brewery_1_etag = brewery_1 = None
    beer_1_id = beer_1_etag = beer_1 = None
    beer_2_id = beer_2_etag = beer_2 = None


    def test_create_brewery(application):
        """this tests create the brewery method"""
        with application.app_context():
            brewery = Brewery(name="18th Street Brewery")
            db.session.add(brewery)
            db.session.commit()

            assert brewery.name == "18th Street Brewery"



    def test_brewery_post(self, test_client):
            """ADD BREWERY"""
            TestApi.author_1 = {
                "name": "18th Street Brewery",
                "id": "1",
            }
            headers_jwt = {
                'Authorization': 'Bearer {}'.format(TestApi.jwt_token)
            }

            ret = test_client.post(BREWERIES_URL, json=TestApi.brewery_1, headers=headers_jwt)
            assert ret.status_code == 201
            ret_val = ret.json
            TestApi.brewery_1_id = ret_val.pop('id')
            TestApi.brewery_1_etag = ret.headers['ETag']
            assert ret_val == TestApi.brewery_1



