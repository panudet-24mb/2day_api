from functools import wraps
from sanic import response
import os
import jwt
import json

def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = await check_request_for_authorization_status(request)
            if token:
                access_token = token.split(" ")[1]
                try:
                    user_payload =  jwt.decode(access_token, os.getenv('SECRET_KEY') )
                    current_token = await check_blacklist(user_payload , request.app.pg)
                    if access_token != current_token:
                        return response.json({'status': 'token_blacklist'}, 401)
                except Exception as e :
                    print(e)
                    return response.json({'status': 'not_authorized'}, 401)
                res = await f(request,user_payload, *args, **kwargs)
                return res
            else:
                return response.json({'status': 'not_authorized'}, 401)
        return decorated_function
    return decorator


async def check_request_for_authorization_status(request):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
        return token
    else:
        return None
    

async def check_blacklist(payload , conn):
    users_id = payload['users_id']
    async with conn.acquire() as connection:
        async with connection.transaction():
            await connection.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
                )
            query = (" select token from token "
            " where users_id = $1 "
            " order by token_id desc " 
            " limit 1")
            result = await connection.fetchrow(query ,int(users_id))
            json_data = json.dumps(result , cls=UUIDEncoder)
    return json.loads(json_data)

                
                

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
    
