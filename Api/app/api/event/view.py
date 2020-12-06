
from sanic import response , Blueprint
import asyncpg
from sanic.log import logger
import jwt
import json
from app.utils.jwt import *
from app.utils.validate_response import *
import datetime, pytz
from dateutil import parser as dateutil_parser
from .service import * 
from app.utils.json import  UUIDEncoder
tz = pytz.timezone('Asia/Bangkok')

event_service = Blueprint(name="event_service")


@event_service.route("/event/init" , methods=['GET'])
@authorized()
async def init_state (req,current_user):
    res = await init_state_check(current_user)
    return await response_json(res)

@event_service.route("/event/attendance" , methods=['POST'])
@authorized()
async def attendance_state (req , current_user):
    rv = await insertAttendance(req,current_user)
    json_data = json.dumps(rv , cls=UUIDEncoder)
    data = json.loads(json_data)
    return await response_json(data)

@event_service.route("/event/history/attendance/<month>/years" , methods=['POST'])
@authorized()
async def attendance_state (req , current_user , month):
    rv = await FindUsersAttendance(current_user , month)
    json_data = json.dumps(rv , cls=UUIDEncoder)
    data = json.loads(json_data)
    return await response_json(data)
    