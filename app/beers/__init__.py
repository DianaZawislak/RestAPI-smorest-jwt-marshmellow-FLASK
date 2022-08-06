import os
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import marshmallow
import pandas as pd
from flask.views import MethodView
from flask_smorest import Blueprint, Page, abort
from app.db.models import Brewery, Beer
from app.db import db
from marshmallow import Schema, fields, EXCLUDE
from marshmallow_sqlalchemy import field_for
from app.extensions import Schema, AutoSchema, SQLCursorPage
from flask_jwt_extended import jwt_required

beers = Blueprint('Beers and Breweries', __name__, url_prefix="/", description="Beers by brewery")


class BrewerySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()

    class Meta:
        type_ = "Brewery"
        strict = True

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


class BreweryNameUpdateSchema(Schema):
    name = fields.Str()


class BeerNameUpdateSchema(Schema):
    name = fields.Str()


@beers.route('/brewery')
class Breweries(MethodView):

    @beers.etag
    @beers.response(200, BrewerySchema(many=True))
    @beers.doc(description="Return ALL Breweries from database", summary="Finds all breweries")
    def get(self):
        """List Breweries"""
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


@beers.route("/brewery/<string:brewery_id>")
class BreweriesById(MethodView):
    @beers.doc(description="Return Breweries based on ID", summary="Finds breweries by ID")
    @jwt_required()
    @beers.response(200, BrewerySchema)
    def get(self, brewery_id):
        """Breweries by ID"""
        brewery = Brewery.query.get_or_404(brewery_id)
        return brewery

    #@beers.arguments(BreweryNameUpdateSchema)
    @beers.doc(security=[{"bearerAuth": []}])
    @beers.etag
    @beers.arguments(BrewerySchema, location="json")
    @beers.response(200, BrewerySchema)
    def put(self, new_item, item_id):
        """Update an existing member"""
        item = Brewery.query.get_or_404(item_id)
        beers.check_etag(item, BrewerySchema)
        BrewerySchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item, {"message": "Brewery name updated"}, 200

    @beers.doc(security=[{"bearerAuth": []}])
    def delete(self, brewery_id):
        brewery = Brewery.query.get_or_404(brewery_id)
        db.session.delete(brewery)
        db.session.commit()
        return {"message": "Brewery deleted"}, 200


@beers.route("/beers")
class Beers(MethodView):

    @beers.etag
    @beers.response(200, BeerSchema(many=True))
    @beers.doc(description="Return ALL beers from database", summary="Finds all beers")
    def get(self):
        """List beers"""
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


@beers.route("/beers/<string:beer_id>")
class BeersById(MethodView):
    @beers.etag
    @beers.doc(description="ReturnBeers based on ID", summary="Finds beers by ID")
    @jwt_required()
    @beers.response(200, BeerSchema)
    def get(self, beer_id):
        """Breweries by ID"""
        beer = Beer.query.get_or_404(beer_id)
        return beer

    @beers.doc(security=[{"bearerAuth": []}])
    def put(self, new_item, item_id):
        """Modify existing beer by ID"""
        item = Beer.query.get_or_404(item_id)
        beers.check_etag(item, BeerSchema)
        BeerSchema().update(item, new_item)
        db.session.add(item)
        db.session.commit()
        return item, {"message": "Beer updated"}, 200

    @beers.doc(security=[{"bearerAuth": []}])
    def delete(self, beer_id):
        """Delete ber"""
        beer = Beer.query.get_or_404(beer_id)
        db.session.delete(beer)
        db.session.commit()
        return {"message": "Beer deleted"}, 200
