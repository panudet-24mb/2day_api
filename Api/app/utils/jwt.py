from functools import wraps
from sanic import response
from tortoise.transactions import in_transaction
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
                    current_token = await check_blacklist(user_payload)
                    if access_token != current_token['token']:
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
    

async def check_blacklist(payload ):
    users_id = payload['users_id']
    async with in_transaction() as conn:
        query = (" select token from token "
            " where users_id = $1  and token_active = true "
            " order by token_id desc " 
            " limit 1")
        system_token = await conn.execute_query_dict(
            query,[int(users_id)]
        )
        
    return system_token[0]
