from django.conf import settings
from .models import *






class Common:
    

    @staticmethod
    def create_payload(status, message, error, data):
        payload = {
            "status": status,
            "message": message,
            "error": error,
            "data": data
        }
        return payload