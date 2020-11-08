from tortoise.transactions import in_transaction
import datetime, pytz
from app.utils.validate_response import  response_json
from app.utils.sql_helper import sql_update_builder
from dateutil import parser
from app.utils.json import  UUIDEncoder
import json
import uuid
tz = pytz.timezone('Asia/Bangkok')



async def FindAll(user_id , params):
    try:
        async with in_transaction() as conn:
            query = (   " select * from news  as n "
            " left join company_has_users as chu on chu.company_id = n.company_id  " 
            " where chu.users_id = $1 and chu.is_active = true and n.delete_at  IS NULL  order by n.news_id DESC  " + params
            )
            find_all = await conn.execute_query_dict(
                query ,[int(user_id) , ]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
        return ({
        "status" : "Success" ,
        "message" :  { "news" : data} , 
        "status_code" : 200
        })  

    except Exception as e:
        print(e)
        return e


async def FindOne(user_id ,  id ):
    try:
        async with in_transaction() as conn:
            query = (   " select * from news  as n "
            " left join company_has_users as chu on chu.company_id = n.company_id  " 
            " where chu.users_id = $1 and chu.is_active = true and n.delete_at  IS NULL and n.news_id = $2   "
            )
            find_all = await conn.execute_query_dict(
                query ,[int(user_id) ,int(id) ]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
        return ({
        "status" : "Success" ,
        "message" :  { "news" : data} , 
        "status_code" : 200
        })  

    except Exception as e:
        print(e)
        return e

async def FindAll_Announcement(user_id , params):
    try:
        async with in_transaction() as conn:
            query = (   " select * from announcement  as n "
            " left join company_has_users as chu on chu.company_id = n.company_id  " 
            " where chu.users_id = $1 and chu.is_active = true and n.delete_at  IS NULL  order by n.announcement_id DESC  " + params
            )
            find_all = await conn.execute_query_dict(
                query ,[int(user_id) , ]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
        return ({
        "status" : "Success" ,
        "message" :  { "news" : data} , 
        "status_code" : 200
        })  

    except Exception as e:
        print(e)
        return e


async def FindOne_Announcement(user_id , params):
    try:
        async with in_transaction() as conn:
            query = (   " select * from announcement  as n "
            " left join company_has_users as chu on chu.company_id = n.company_id  " 
            " where chu.users_id = $1 and chu.is_active = true and n.delete_at  IS NULL   and n.announcement_id = $2  " 
            )
            find_all = await conn.execute_query_dict(
                query ,[int(user_id) ,int(params) ]
             )
            json_data = json.dumps(find_all , cls=UUIDEncoder)    
            data =  json.loads(json_data)
        return ({
        "status" : "Success" ,
        "message" :  { "news" : data} , 
        "status_code" : 200
        })  

    except Exception as e:
        print(e)
        return e
    