from sanic import Blueprint
from app.api.authentication.view import authentication_service
from app.api.employee.view import employee_service
from app.api.news.view import news_service
from app.api.beacon.view import beacon_service
from app.api.event.view import event_service
api = Blueprint.group(authentication_service,employee_service , news_service,beacon_service,event_service, url_prefix='/api/v1')
