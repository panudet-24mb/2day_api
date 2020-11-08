
from sanic import response , Blueprint
import asyncpg
from sanic.log import logger
import jwt
import json
from app.utils.jwt import *
import datetime, pytz
from dateutil import parser as dateutil_parser
tz = pytz.timezone('Asia/Bangkok')

employee_service = Blueprint(name="employee_service")

@employee_service.route("/test" , methods=['GET'])
@authorized()
async def test (req,current_user):
    return response.text('ok')
    