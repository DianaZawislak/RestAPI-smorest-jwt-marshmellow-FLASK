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


class BeerUpdateSchema(Schema):
    name = fields.Str()
    id = fields.Integer()


class BreweryUpdateSchema(Schema):
    name = fields.Str()
    id = fields.Integer()


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
    @beers.response(200, BrewerySchema)
    def get(self, brewery_id):
        """Breweries by ID"""
        brewery = Brewery.query.get_or_404(brewery_id)
        return brewery

    @beers.arguments(BreweryUpdateSchema)
    @beers.response(200, BrewerySchema)
    @beers.doc(description="Updates Brewery based on ID", summary="Updates brewery by ID")
    def put(self, item_data, brewery_id):
        """update brewery"""
        item = Brewery.query.get_or_404(brewery_id)

        if item:
            item.price = item_data["id"]
            item.name = item_data["name"]
        else:
            item = Brewery(**item_data)

        db.session.add(item)
        db.session.commit()

        return item, {"message": "Brewery updated"}, 200

    @beers.doc(security=[{"bearerAuth": []}])
    @beers.doc(description="Deletes Brewery based on ID", summary="Deletes brewery by ID")
    def delete(self, brewery_id):
        """delete brewery"""
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
    def post(self, new_item):
        """Add a Beer"""

        item = Beer(**new_item)
        db.session.add(item)
        db.session.commit()
        return item


@beers.route("/beers/<string:beer_id>")
class BeersById(MethodView):
    @beers.etag
    @beers.doc(description="Returns Beers based on ID", summary="Finds beers by ID")
    @beers.response(200, BeerSchema)
    def get(self, beer_id):
        """Breweries by ID"""
        beer = Beer.query.get_or_404(beer_id)
        return beer

    @beers.doc(description="Updates Beers based on ID", summary="Updates beers by ID")
    @beers.arguments(BeerUpdateSchema)
    @beers.response(200, BeerSchema)
    def put(self, item_data, beer_id):
        item = Beer.query.get_or_404(beer_id)

        if item:
            item.price = item_data["id"]
            item.name = item_data["name"]
        else:
            item = Beer(**item_data)

        db.session.add(item)
        db.session.commit()

        return item, {"message": "Beer updated"}, 200

    @beers.doc(description="Deletes Beers based on ID", summary="Deletes beers by ID")
    @beers.doc(security=[{"bearerAuth": []}])
    def delete(self, beer_id):
        """Delete ber"""
        beer = Beer.query.get_or_404(beer_id)
        db.session.delete(beer)
        db.session.commit()
        return {"message": "Beer deleted"}, 200
