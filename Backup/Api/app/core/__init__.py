import os
from sanic import Sanic
from simple_bcrypt import Bcrypt
from sanic_cors import CORS, cross_origin
from app.db.postgres import config as DBconfig
from app.api.api import api
from tortoise.contrib.sanic import register_tortoise


def create_app():
    app = Sanic(__name__)
    app.blueprint(api)
    bcrypt = Bcrypt(app)
    register_tortoise(app, generate_schemas=False ,config = DBconfig )
    CORS(app, automatic_options=True)
    return app




