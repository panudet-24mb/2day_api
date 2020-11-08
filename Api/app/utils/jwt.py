from functools import wraps
from sanic.response import json
from tortoise.transactions import in_transaction
import os
import jwt

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
					if access_token != current_token['system_token']:
						return json({'status': 'token_blacklist'}, 401)
				except Exception as e :
					return json({'status': 'not_authorized'}, 401)
				response = await f(request,user_payload, *args, **kwargs)
				return response
			else:
				return json({'status': 'not_authorized'}, 401)
		return decorated_function
	return decorator


async def check_request_for_authorization_status(request):
	token = None
	if "Authorization" in request.headers:
		token = request.headers["Authorization"]
		return token
	else:
		return None
	

async def check_blacklist(payload):
	member_public_id = payload['member_public_id']
	async with in_transaction() as conn:
		system_token = await conn.execute_query_dict(
			" select system_token from system_token "
			" where member_public_id = $1 "
			" order by system_token_id desc " 
			" limit 1" ,
			[member_public_id]
		)
	return system_token[0]
				