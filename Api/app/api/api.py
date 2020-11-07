from sanic import Blueprint
from app.api.authentication.view import authentication_service


api = Blueprint.group(authentication_service, url_prefix='/api/v1')
