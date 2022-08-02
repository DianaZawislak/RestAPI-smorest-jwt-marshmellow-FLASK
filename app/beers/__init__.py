import os

import marshmallow
import pandas as pd
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, Page
from app.db.models import Brewery, Beer
from app.db import db
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_sqlalchemy import field_for
from app.extensions import Schema, AutoSchema, SQLCursorPage

beers = Blueprint('Beers and Breweries', __name__, url_prefix="/", description="Beers by brewery")


class BrewerySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    class Meta(AutoSchema.Meta):
        table = Brewery.__table__

    def update(self, item, new_item):
        pass


class BeerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    brewery_id = fields.Integer()

    class Meta:
        type_ = "Beer"
        strict = True

    def update(self, item, new_item):
        pass


class BreweryQueryArgsSchema(Schema):
    brewery_id = marshmallow.fields.Int()


class BeerQueryArgsSchema(Schema):
    beer_id = marshmallow.fields.Int()


@beers.route('/breweries')
class Breweries(MethodView):

    @beers.etag
    @beers.arguments(BreweryQueryArgsSchema, location='query')
    @beers.response(200, BrewerySchema(many=True))
    def get(self, args):
        """List Countries"""
        # ret = Brewery.query.all()
        beer_id = args.pop('beer_id', None)
        ret = Brewery.query.filter_by(**args)
        if beer_id is not None:
            ret = ret.join(Brewery.beers).filter(Beer.id == beer_id)
        return ret

    @beers.etag
    @beers.arguments(BrewerySchema)
    @beers.response(201, BrewerySchema)
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    def post(self, new_item):
        """Add a Brewery"""

        item = Brewery(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@beers.route('/breweries:id')
class BreweryById(MethodView):

    @beers.etag
    @beers.response(201, BrewerySchema)
    def get(self, item_id):
        """Brewery by ID"""
        return Brewery.query.get_or_404(item_id)

    @beers.etag
    @beers.arguments(BrewerySchema, location="json")
    @beers.response(201, BrewerySchema)
    @beers.doc(parameters=[{'name': 'If-Match', 'in': 'header', 'required': 'true'}])
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required
    def put(self, new_item, item_id):
        """Update Brewery"""
        item = Brewery.query.get_or_404(item_id)
        beers.check_etag(item, BrewerySchema)
        BrewerySchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item

    @beers.etag
    @beers.response(204)
    @beers.doc(parameters=[{'name': 'If-Match', 'in': 'header', 'required': 'true'}])
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required
    def delete(self, item_id):
        """Delete Brewery"""
        item = Brewery.query.get_or_404(item_id)
        beers.check_etag(item, BrewerySchema)
        db.session.delete(item)
        db.session.commit()


@beers.route('/beers')
class Beers(MethodView):

    @beers.etag
    @beers.arguments(BeerQueryArgsSchema, location='query')
    @beers.response(200, BeerSchema(many=True))
    def get(self, args):
        """List Beers"""
        return Beer.query.filter_by(**args)

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


@beers.route('/beers:id')
class BeerById(MethodView):

    @beers.etag
    @beers.response(201, BeerSchema(many=True))
    def get(self, item_id):
        """Beers by ID"""
        return Beers.query.get_or_404(item_id)

    @beers.etag
    @beers.arguments(BeerSchema, location="json")
    @beers.response(201, BeerSchema)
    @beers.doc(parameters=[{'name': 'If-Match', 'in': 'header', 'required': 'true'}])
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required
    def put(self, update_data, beer_id):
        """Update existing beer"""
        item = Beer.get_by_id(beer_id)
        item.update(update_data)
        item.commit()
        return item

    @beers.etag
    @beers.response(204)
    @beers.doc(parameters=[{'name': 'If-Match', 'in': 'header', 'required': 'true'}])
    @beers.doc(security=[{"bearerAuth": []}])
    @jwt_required
    def delete(self, item_id):
        """Delete Beers"""
        item = Beers.query.get_or_404(item_id)
        beers.check_etag(item, BeerSchema)
        db.session.delete(item)
        db.session.commit()
