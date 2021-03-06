from sanic import response , Blueprint
import os
import asyncpg
from sanic.log import logger
import jwt
import json
from app.utils.validate_request import check_content_type
import datetime, pytz
from dateutil import parser as dateutil_parser
tz = pytz.timezone('Asia/Bangkok')

authentication_service = Blueprint(name="authentication_service")

@authentication_service.route("/check-user" , methods=['POST'])
async def check_user(req):
    try:
        params = req.json 
        async with req.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
                )
            async with connection.transaction():
                query_exist_user = ('select * from users as a left join userdetails as b on a.users_id = b.users_id  where a.users_citizen_id = $1')
                results = await connection.fetch(query_exist_user ,str(params["citizen_id"]))
                return response.json({"payload" :  jsonify(results)})
    except Exception as e :
        print(e)
        return response.json({'error':'error'})

def jsonify(records):
    return [dict(r.items()) for r in records]

import json
from uuid import UUID
import datetime
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    



@authentication_service.route("/sign-in" , methods=['POST'])
async def sign_in(req):
    try : 
        now = datetime.datetime.now(tz)
        timestamp = datetime.datetime.timestamp(now)
        dt = now.replace(tzinfo=None)
        params = req.json 
        if "citizen_id" not in params.keys():
            return response.json({
                "status" : "error" , 
                "payload" :  "ต้องการรหัสบัตรประชาชน" , 
                } , status =  400
                )
        
        async with req.app.pg.acquire() as connection:
            async with connection.transaction():
                await connection.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
                )
                query_exist_user = ('select * from users where users_citizen_id = $1')
                result = await connection.fetchrow(query_exist_user ,str(params["citizen_id"]))
                if not result :
                    return response.json({
                        "status" : "error" , 
                        "payload" :  "รหัสบัตรประชาชนนี้ยังไม่ถูกเปิดใช้งาน" , 
                        } , status =  401
                        )
                users_id = result["users_id"]
                users_uuid = result["users_uuid"]
                query_check_token = ('select * from token where users_id = $1 and token_active = true order by token_id desc limit 1 ')
                result_token = await connection.fetchrow(query_check_token ,int(users_id))
                if result_token :
                    return response.json({
                        "status" : "error" , 
                        "payload" :  "รหัสบัตรประชาชนนี้ถูกใช้งานบนเครื่อง Device อื่น" , 
                        } , status =  400
                        )
                if not result_token:
                    token = jwt.encode({'users_uuid' : str(users_uuid),'users_id' : str(users_id) ,'created' : timestamp }, os.getenv('SECRET_KEY'))
                    token = token.decode('UTF-8')
                    insert_token_query = (' insert into token (users_id ,token,token_created,token_active) values ($1,$2,$3,$4)')
                    result_inert_token = await connection.execute(insert_token_query ,int(users_id) ,str(token) , dt , True)
                    return response.json({
                        'token' : token
                    } , status= 200)
    except Exception as e :
        print(e)
        return response.json({
                        "status" : "error" , 
                        "payload" :  "server error" , 
                        } , status =  500
                        )