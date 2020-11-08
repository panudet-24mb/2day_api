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
        query_exist_user = ( ' select * from users as a '
                                ' left join company_has_users as b '
                                ' on a.users_id = b.users_id '
                                ' left join company_has_usersdetails as c on b.comapny_has_users_id = c.comapny_has_users_id '
                                ' left join userdetails as ud on ud.userdetails_id = c.userdetails_id '
                                ' left join department as d on d.department_id = ud.department_id  '
                                ' left join position as p '
                                ' on p.position_id = ud.position_id where a.users_citizen_id = $1 '
                                ' AND c.is_active = true and b.is_active = true limit 1 ORDER by c.company_has_users_details_id DESC LIMIT 1 '
                            )
        async with in_transaction() as conn:
            users_data = await conn.execute_query_dict(
            query_exist_user,[str(params["citizen_id"])] 
            )
            if users_data  :
                json_data = json.dumps(users_data , cls=UUIDEncoder)    
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