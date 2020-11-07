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
    
