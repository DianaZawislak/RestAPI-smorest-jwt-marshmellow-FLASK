import os

import marshmallow
import pandas as pd
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, Page
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy_utils.types import country

from app.db.models import Country, City
from app.db import db
from marshmallow import Schema, fields, EXCLUDE

geography = Blueprint('Geography - Countries and Cities', __name__, url_prefix="/",
                      description="Operations on Locations")


class CountrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    class Meta:
        type_ = "Country"
        strict = True

    def update(self, item, new_item):
        pass


class CitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    country_id = fields.Int()

    class Meta:
        type_ = "City"
        strict = True

    def update(self, item, new_item):
        pass


@geography.route('/countries')
class Countries(MethodView):

    @geography.etag
    @geography.response(200, CountrySchema(many=True))
    def get(self):
        """List Countries"""
        ret = Country.query.all()

        return ret

    @geography.etag
    @geography.arguments(CountrySchema, location="json")
    @geography.response(201, CountrySchema)
    @geography.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        """Add a Country"""

        item = Country(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@geography.route('/countries/<string:country_id>')
class BeerById(MethodView):
    @geography.doc(description="Return Countries based on ID", summary="Finds country by ID")
    @jwt_required()
    @geography.response(200, CountrySchema)
    def get(self, country_id):
        """Beers by ID"""
        country = Country.query.get_or_404(country_id)
        return country

    @geography.doc(security=[{"bearerAuth": []}])
    def put(self, new_item, item_id):
        """Modify existing country by ID"""
        item = Country.query.get_or_404(item_id)
        geography.check_etag(item, CountrySchema)
        CountrySchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item, {"message": "Country updated"}, 200

    @geography.doc(security=[{"bearerAuth": []}])
    def delete(self, country_id):
        """Delete country"""
        country = Country.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        return {"message": "Country deleted"}, 200


@geography.route('/cities')
class Cities(MethodView):

    @geography.etag
    @geography.response(200, CitySchema(many=True))
    @geography.doc(description="Return ALL cities from database", summary="Finds all cities")
    def get(self):
        """List Cities"""
        ret = City.query.all()

        return ret

    @geography.etag
    @geography.arguments(CitySchema, location="json")
    @geography.response(201, CitySchema)
    @geography.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        """Add a City"""
        item = City(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@geography.route("/cities/<string:city_id>")
class CityById(MethodView):

    @geography.etag
    @geography.doc(description="Returns cities based on ID", summary="Finds city by ID")
    @jwt_required()
    @geography.response(200, CitySchema)
    def get(self, city_id):
        """City by ID"""
        city = City.query.get_or_404(city_id)
        return city

    @geography.etag
    @geography.arguments(CitySchema, location="json")
    @geography.response(201, CitySchema)
    @geography.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def put(self, new_item):
        """Update a City"""
        item = City(**new_item)
        db.session.update(item)
        db.session.commit()
        return item, {"message": "City updated"}

    def delete(self, city_id):
        """Delete City"""
        city = City.query.get_or_404(city_id)
        db.session.delete(city)
        db.session.commit()
        return {"message": "City deleted"}, 200
