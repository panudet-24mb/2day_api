import os
from sanic import Sanic 
from sanic.blueprints import Blueprint
from simple_bcrypt import Bcrypt
from sanic_cors import CORS, cross_origin
from app.db.db import config as DBconfig
from tortoise.contrib.sanic import register_tortoise
from sanic_limiter import Limiter, get_remote_address


def create_app():
    app = Sanic(__name__)
    # Limiter(app, global_limits=['60 per minute'], key_func=get_remote_address)
    register_tortoise(app, generate_schemas=False ,config = DBconfig )
    bcrypt = Bcrypt(app)
    app.static('/static', './static')
    static_file_bp = Blueprint('static', url_prefix='/static')
    # CORS(app, automatic_options=True)
    return app