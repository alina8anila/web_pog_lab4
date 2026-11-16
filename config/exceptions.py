import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger("config.exceptions")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get("request")
    method = getattr(request, "method", "-")
    path = getattr(request, "path", "-")
    user_id = getattr(getattr(request, "user", None), "id", None)

    if response is None:
        logger.error(
            "unhandled exception %s %s user_id=%s",
            method,
            path,
            user_id,
            exc_info=exc,
        )
        return None

    status_code = response.status_code
    details = {}

    if status_code == 400:
        message = "Невалідні дані."
        details = response.data
    elif status_code == 401:
        if isinstance(exc, InvalidToken):
            message = "Токен недійсний або прострочений. Увійдіть повторно."
        elif isinstance(exc, AuthenticationFailed):
            message = "Невірний username або пароль."
        else:
            message = (
                "Потрібна автентифікація. "
                "Передайте access-токен у заголовку Authorization."
            )
    elif status_code in (403, 409):
        message = str(exc.detail)
    elif status_code == 404:
        message = "Об'єкт не знайдено."
    elif status_code == 405:
        message = "Метод не дозволений для цього ресурсу."
    else:
        message = "Помилка запиту."

    response.data = {
        "error": {
            "message": message,
            "details": details,
        }
    }
    if status_code == 400:
        fields = sorted(details) if isinstance(details, dict) else ["non_field_errors"]
        logger.warning(
            "%s %s status=400 fields=%s user_id=%s",
            method,
            path,
            fields,
            user_id,
        )
    else:
        logger.warning(
            "%s %s status=%s user_id=%s",
            method,
            path,
            status_code,
            user_id,
        )

    return response
