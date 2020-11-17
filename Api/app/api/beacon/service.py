from tortoise.transactions import in_transaction
import datetime, pytz
from app.utils.validate_response import  response_json
from app.utils.sql_helper import sql_update_builder
from dateutil import parser
from app.utils.json import  UUIDEncoder
import json
import uuid

tz = pytz.timezone('Asia/Bangkok')

async def FindUsersCompany(user_id):
    try:
        async with in_transaction() as conn:
            query = (   " select * from company_has_users as chu "
                     " where users_id = $1 and is_active = true order by chu.company_has_users_id DESC LIMIT 1 "
            )
            find_all = await conn.execute_query_dict(
                query,[int(user_id)]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
            company_id = data[0]['company_id']
            return company_id
    except Exception as e:
        print(e)
        return e
    
async def FindAll(user_id):
    try:
        users_company_id = await FindUsersCompany(user_id)
        async with in_transaction() as conn:
            query = (   " select c.company_id , b.beacon_id , b.beacon_unique_uuid , b.beacon_service_uuid , b.beacon_characteristic_uuid from beacon as b  " 
                        " left join company_has_beacon as chb on "
                        " chb.beacon_id = b.beacon_id "
                        " left join company as c on " 
                        " c.company_id = chb.company_id "
                        " left join company_has_users as chu on "
                        " chu.company_id = c.company_id  where c.company_id = $1 "
                        " and b.delete_at is null and b.is_active = true and chb.is_active = true and chb.delete_at is null "
            )
            find_all = await conn.execute_query_dict(
                query,[int(users_company_id)]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
        return ({
        "status" : "Success" ,
        "message" :  { "Beacon" : find_all } , 
        "status_code" : 200
        })  
    except Exception as e:
        print(e)
        return e

