from sanic import Blueprint
from app.api.authentication.view import authentication_service
from app.api.employee.view import employee_service

api = Blueprint.group(authentication_service,employee_service , url_prefix='/api/v1')
