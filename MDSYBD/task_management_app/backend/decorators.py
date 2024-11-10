# decorators.py

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_restx import abort


def role_required(required_roles):
    """
    Декоратор для проверки роли пользователя.
    :param required_roles: Список ролей, которые имеют доступ к эндпоинту.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in required_roles:
                abort(403, "Доступ запрещен: недостаточно прав")
            return fn(*args, **kwargs)

        return wrapper

    return decorator
