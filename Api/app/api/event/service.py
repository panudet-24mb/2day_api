from tortoise.transactions import in_transaction
import datetime, pytz
from app.utils.validate_response import  response_json
from app.utils.sql_helper import sql_update_builder
from dateutil import parser
from app.utils.json import  UUIDEncoder
import json
import uuid

tz = pytz.timezone('Asia/Bangkok')

async def init_state_check(current_user):
    try:
        dt = datetime.datetime.now(tz)
        async with in_transaction() as conn:
            query = (   
                    " select * from attendance as a where  a.attendance_date = $1 and a.users_uuid_id = $2 order by attendance_id DESC limit 2  "
            )
            rv = await conn.execute_query_dict(
                query,[ dt.date(), current_user["users_uuid"] ]
             )
            if not rv:
                return ({
                "status" : "success" ,
                "message" :  { "attendance_init" :  0  , "message" : "empty attendance" } , 
                "status_code" : 200
                })  
            else:
                if (rv[0]['attendance_type_id'] == 1 ):
                    return ({
                    "status" : "success" ,
                    "message" :  { "attendance_init" : 1  ,
                        "attendance_date" : str(rv[0]['attendance_date'])  ,
                                  "attendance_time" : str(rv[0]['attendance_time']),
                                  "attendance_type_id" : str(rv[0]['attendance_type_id']),
                                   "attendance" : "already checkin"} , 
                    "status_code" : 200
                    })  
                if (rv[0]['attendance_type_id'] == 2  ):
                    return ({
                    "status" : "success" ,
                    "message" :  { "attendance_init" : 2,
                        "attendance_date" : str(rv[0]['attendance_date'])  ,
                                "attendance_details" : rv,
                                  "attendance" : "attendance success"} , 
                    "status_code" : 200
                    })  
                    
    except Exception as e:
        print(e)
        return ({
            "status" : "Failed" ,
            "message" :  { "message" : "Failed" } , 
            "status_code" : 400
            })  
async def insertAttendance(req , current_user):
    try:
        params = req.json
        dt = datetime.datetime.now(tz)
        uuid_entry = str( uuid.uuid4() ) 
        async with in_transaction() as conn:
            query = (   
                     " INSERT INTO attendance ( "
                     " attendance_public_id, attendance_date, attendance_time, attendace_remark, attendance_location, attendance_lat, attendance_long, created, is_active, attendance_method_id, attendance_type_id, users_uuid_id) VALUES "
                     " ($1 , $2 , $3 , $4 , $5 , $6 ,$7 , $8 ,$9 ,$10 ,$11 ,$12 ) "
                     " returning attendance_id;"
            )
            await conn.execute_query(
                query,[ uuid_entry ,dt.date() , dt.time() , params["attendance_remark"], params["attendance_location"] ,  str(params["attendance_lat"]), str(params["attendance_long"]),dt , True ,  params["attendance_method_id"] ,  params["attendance_type_id"] , current_user["users_uuid"] ]
             )
        return ({
        "status" : "Success" ,
        "message" :  { "message" : "success" } , 
        "status_code" : 201
        })  
    except Exception as e:
        print(e)
        return ({
            "status" : "Failed" ,
            "message" :  { "message" : "Failed" } , 
            "status_code" : 400
            })  
async def FindUsersAttendance(current_user , month ,years):
    try:
        dt = datetime.datetime.now(tz)
        async with in_transaction() as conn:
            query_checkin = (   
                    " select * from attendance as a  "
                    " where DATE_PART('month' ,a.attendance_date) = $1 "
                    " AND DATE_PART( 'year',a.attendance_date) = $2 and a.users_uuid_id = $3 and a.attendance_type_id = 1 order by attendance_id ASC "
            )
            rv_checkin = await conn.execute_query_dict(
                query_checkin,[ int(month), int(years) , current_user["users_uuid"]  ]
             )
            query_checkout = (   
                    " select * from attendance as a  "
                    " where DATE_PART('month' ,a.attendance_date) = $1 "
                    " AND DATE_PART( 'year',a.attendance_date) = $2 and a.users_uuid_id = $3 and a.attendance_type_id = 2 order by attendance_id ASC "
            )
            rv_checkout = await conn.execute_query_dict(
                query_checkout,[ int(month), int(years) , current_user["users_uuid"]  ]
             )
            
            
            
          
    
            return ({
                "status" : "success" ,
                "message" :  { "message" : "rv" } , 
                "status_code" : 200
                })  
                    
    except Exception as e:
        print(e)
        return ({
            "status" : "Failed" ,
            "message" :  { "message" : "Failed" } , 
            "status_code" : 400
            })  
    