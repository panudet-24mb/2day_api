
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

beacon_service = Blueprint(name="beacon_service")
@beacon_service.route("/beacon" , methods=['GET'])
@authorized()
async def get_beacon_company (req,current_user):
    user_id = current_user['users_id']
    res = await FindAll(user_id)
    return await response_json(res)
    