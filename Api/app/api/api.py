from sanic import Blueprint
from app.api.authentication.view import authentication_service
from app.api.employee.view import employee_service
from app.api.news.view import news_service
api = Blueprint.group(authentication_service,employee_service , news_service, url_prefix='/api/v1')
