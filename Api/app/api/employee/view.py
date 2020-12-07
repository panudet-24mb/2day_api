
from sanic import response , Blueprint
from tortoise.transactions import in_transaction
import asyncpg
from sanic.log import logger
import jwt
import json
from app.utils.jwt import *
import datetime, pytz
from dateutil import parser as dateutil_parser
from app.utils.json import  UUIDEncoder
tz = pytz.timezone('Asia/Bangkok')

employee_service = Blueprint(name="employee_service")

@employee_service.route("/employee/health_check" , methods=['GET'])
@authorized()
async def health_check (req,current_user):
    return response.json({'message ' : 'ok'})


@employee_service.route("/employee/profile" , methods=['GET'])
@authorized()
async def employee_profile (req,current_user):
    try:
        query_exist_user = ( ' select * from users as a '
                                ' left join company_has_users as b '
                                ' on a.users_id = b.users_id '
                                ' left join company_has_usersdetails as c on b.company_has_users_id = c.company_has_users_id '
                                ' left join userdetails as ud on ud.userdetails_id = c.userdetails_id '
                                ' left join department as d on d.department_id = ud.department_id  '
                                ' left join position as p '
                                ' on p.position_id = ud.position_id where a.users_uuid = $1 '
                                ' AND c.is_active = true and b.is_active = true  ORDER by c.company_has_users_details_id DESC LIMIT 1 '
                            )
        async with in_transaction() as conn:
            users_data = await conn.execute_query_dict(
            query_exist_user,[str(current_user["users_uuid"])] 
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
        return response.json({'error':'error'}, status = 500)
