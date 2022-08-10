"""utilities"""
import jwt

from flask_jwt_extended.config import config

#pylint: disable=consider-using-f-string


def encode_token(app, token_data, headers=None):
    """encode token"""
    with app.test_request_context():
        return jwt.encode(
            token_data,
            config.decode_key,
            algorithm=config.algorithm,
            json_encoder=config.json_encoder,
            headers=headers,
        )


def get_jwt_manager(app):
    """get jwt manager"""
    return app.extensions["flask-jwt-extended"]


def make_headers(jwt):
    """make headers"""
    return {"Authorization": "Bearer {}".format(jwt)}
