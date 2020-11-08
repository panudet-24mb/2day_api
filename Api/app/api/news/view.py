
from sanic import response , Blueprint
import asyncpg
from sanic.log import logger
import jwt
import json
from app.utils.jwt import *
import datetime, pytz
from dateutil import parser as dateutil_parser
from .service import * 
tz = pytz.timezone('Asia/Bangkok')


news_service = Blueprint(name="news_service")

@news_service.route("/news" , methods=['GET'])
@authorized()
async def get_news (req,current_user):
    _args = req.args
    _default = " "
    _params = _default
    if "limit"  in _args :
        limit = _args['limit'][0]
        _params = " limit " + str(limit)
    res = await FindAll(current_user["users_id"] , _params )
    return await response_json(res)

@news_service.route("/news/<id>" , methods=['GET'])
@authorized()
async def get_news_id (req,current_user,id):
    res = await FindOne(current_user["users_id"] ,id)
    return await response_json(res)
    