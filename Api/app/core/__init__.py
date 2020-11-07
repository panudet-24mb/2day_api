import os
from sanic import Sanic
from simple_bcrypt import Bcrypt
from sanic_cors import CORS, cross_origin
from app.db import postgres
import asyncpg
from app.api.api import api


def create_app():
    app = Sanic(__name__)
    app.blueprint(api)
    bcrypt = Bcrypt(app)
    setup_db(app)
    CORS(app, automatic_options=True)
    return app

def setup_db(app):
    @app.listener('before_server_start')
    async def setup_db(app, loop):
        app.pg = await postgres.create_connection_pool()
        
    @app.listener('after_server_stop')
    async def close_db(app, loop):
        await app.pg.close()
        


