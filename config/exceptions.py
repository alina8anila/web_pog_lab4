from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class Conflict(APIException):
    status_code = 409
    default_detail = "Конфлікт із поточним станом ресурсу."


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    code = response.status_code

    if code == 400:
        message = "Невалідні дані."
    elif code == 404:
        message = "Об'єкт не знайдено."
    elif code == 409:
        message = str(exc.detail)
    else:
        message = "Помилка запиту."

    response.data = {
        "error": {
            "message": message,
            "details": response.data if code == 400 else {},
        }
    }
    return response