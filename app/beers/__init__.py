import os

import pandas as pd
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, Page
from app.db.models import Country, City
from app.db import db
from marshmallow import Schema, fields, EXCLUDE

beers = Blueprint('beers', __name__, url_prefix="/beers", description="Beers by brewery")


class BrewerySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    class Meta:
        type_ = "Brewery"
        strict = True


class BeerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    brewery_id = fields.Integer()

    class Meta:
        type_ = "Beer"
        strict = True


@beers.route('/breweries')
class Breweries(MethodView):

    @beers.etag
    @beers.response(200, BrewerySchema(many=True))
    def get(self):
        """List Countries"""
        ret = Brewery.query.all()
        return ret

    @beers.etag
    @beers.arguments(BrewerySchema, location="json")
    @beers.response(201, BrewerySchema)
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        """Add a Brewery"""

        item = Brewery(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@beers.route('/beers')
class Breweries(MethodView):

    @beers.etag
    @beers.response(200, BeerSchema(many=True))
    def get(self):
        """List Beers"""
        ret = Beer.query.all()
        return ret

    @beers.etag
    @beers.arguments(BeerSchema, location="json")
    @beers.response(201, BeerSchema)
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        """Add a Beer"""

        item = Beer(**new_item)
        db.session.add(item)
        db.session.commit()
        return item