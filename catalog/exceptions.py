from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class Conflict(APIException):
    status_code = 409
    default_detail = "Конфлікт із поточним станом ресурсу."