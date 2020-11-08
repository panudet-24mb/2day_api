from sanic import response , Blueprint
from tortoise.transactions import in_transaction
import os
from sanic.log import logger
import jwt
import json
from app.utils.validate_response import *
import datetime, pytz
from dateutil import parser as dateutil_parser
from app.utils.json import  UUIDEncoder
tz = pytz.timezone('Asia/Bangkok')


authentication_service = Blueprint(name="authentication_service")



@authentication_service.route("/check-user" , methods=['POST'])
async def check_user(req):
    try:
        params = req.json
        if "citizen_id" not in params.keys():
            return response.json({
                "status" : "error" , 
                "payload" :  "ต้องการรหัสบัตรประชาชน" , 
                } , status =  400
                ) 
        query_exist_user = ('select * from users as a left join userdetails as b on a.users_id = b.users_id left join department as d on d.department_id = b.department_id  left join position as p on p.position_id = b.position_id where a.users_citizen_id = $1')
        async with in_transaction() as conn:
            count_total_users = await conn.execute_query_dict(
            query_exist_user,[str(params["citizen_id"])] 
            )
            if count_total_users  :
                json_data = json.dumps(count_total_users , cls=UUIDEncoder)    
                return response.json({"payload" :  json.loads(json_data)})
            else :
                return response.json({
                "status" : "error" , 
                "payload" :  "ไม่พบข้อมูล" , 
                } , status =  404
                ) 
            
    except Exception as e :
        print(e)
        return response.json({'error':'error'})


    



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
        async with in_transaction() as connection:
            query_exist_user = (" select * from users where users_citizen_id = $1 ")
            result = await connection.execute_query_dict(
                query_exist_user , [ params["citizen_id"] ] 
            )
            if not result :
                return response.json({
                    "status" : "error" , 
                    "payload" :  "รหัสบัตรประชาชนนี้ยังไม่ถูกเปิดใช้งาน" , 
                    } , status =  401
                    )
            users_id = result[0]["users_id"]
            users_uuid = result[0]["users_uuid"]
            query_check_token = ('select * from token where users_id = $1 and token_active = true order by token_id desc limit 1 ')
            result_token = await connection.execute_query_dict(query_check_token ,[int(users_id)])
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
                result_inert_token = await connection.execute_query_dict(insert_token_query ,[int(users_id) ,str(token) , dt , True])
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