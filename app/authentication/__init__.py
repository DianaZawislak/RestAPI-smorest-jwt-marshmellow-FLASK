"""These are the routes to login, register, and protect a route"""
import json
from datetime import datetime
from pprint import pprint
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, current_user, decode_token, create_refresh_token, \
    get_jwt, get_jwt_identity
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, EXCLUDE

from app.db import db
from app.db.models import User

authentication = Blueprint('authentication', __name__, url_prefix="/", description="Operations on users")


class RegisterUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String()
    password = fields.String()

    class Meta:
        type_ = "User"
        strict = True


class RegisterUserResponseSchema(Schema):
    username = fields.String()

    class Meta:
        type_ = "User"
        strict = True


class LoginUserSchemaResponse(Schema):
    access_token = fields.String()


class LoginUserSchemaPost(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String()
    password = fields.String()

    class Meta:
        type_ = "User"
        strict = True


class ProtectedRouteSchema(Schema):
    Authorization = fields.String()


class JWTSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    access_token = fields.Str()
    token_type = fields.Str()
    expires = fields.Str()


class UserUpdateSchema(Schema):
    name = fields.Str()
    id = fields.Integer()


@authentication.route('/register', methods=['POST'])
@authentication.arguments(RegisterUserSchema, location="json")
@authentication.response(201, RegisterUserResponseSchema)
@authentication.doc(description="Register User", summary="Register User")
def register(data):
    """Register a User
    Return a user.
    ---
    Internal comment not meant to be exposed.
    """
    # Check if there are any users.  The first user will be made an admin

    username = data['username']
    password = data['password']
    if User.query.count() == 0:
        user = User(username=username, password=password)
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username, password=password)
        else:
            return jsonify("Already Registered"), 200
    db.session.add(user)
    db.session.commit()
    return user, 201


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@authentication.route("/auth", methods=["POST"])
@authentication.arguments(LoginUserSchemaPost, location="json")
@authentication.response(201, JWTSchema)
@authentication.doc(description="Authorize User/Login", summary="Authorize User/Login")
def login(data):
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        abort(401, message="Invalid Username or Password")
    else:
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=username)
        pure_decoded = decode_token(access_token)
        refresh_token = create_refresh_token(user.id)
        return jsonify(access_token=access_token,
                       token_type='Bearer',
                       refresh_token=refresh_token,
                       expires=datetime.fromtimestamp(pure_decoded["exp"]).strftime('%Y-%m-%d %H:%M:%S')), 200


@authentication.route("/user_info", methods=["GET"])
@authentication.doc(security=[{"bearerAuth": []}])
@jwt_required()
@authentication.doc(description="Get User Info", summary="Get User Info")
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )


# @authentication.route("/user_update", methods=["PUT"])
# @authentication.arguments(UserUpdateSchema)
# @authentication.response(200, RegisterUserSchema)
# @authentication.doc(description="Updates user based on ID", summary="Updates user by ID")
# def put(self, item_data, brewery_id):
# """update user"""
# item = User.query.get_or_404(user_id)

# if item:
# item.id = item_data["id"]
# item.name = item_data["username"]
# else:
# item = User(**item_data)

# db.session.add(item)
# db.session.commit()

# return item, {"message": "User updated"}, 200


@authentication.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        return {"message": "Successfully logged out"}, 200


@authentication.route("/delete_user", methods=["DELETE"])
@authentication.doc(description="Delete User", summary="Delete User")
@authentication.response(200, RegisterUserSchema)
def delete(self, user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}, 200


@authentication.get("/refresh")
@jwt_required(refresh=True)
def refresh_user_token(self):
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return {"access_token": access}, 200
