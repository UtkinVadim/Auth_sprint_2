from functools import wraps
from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app import jwt, models, redis_client


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) -> bool:
    """
    Проверяет наличие токена в редисе, если нет - значит токен истёк

    :param jwt_header:
    :param jwt_payload:
    :return:
    """
    if jwt_payload["type"] != "refresh":
        return False
    token_is_revoked = redis_client.token_is_revoked(user_id=jwt_payload["sub"], jti=jwt_payload["jti"])
    return token_is_revoked


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, jwt_data):
    """
    Callback на случай запроса с истёкшим токеном. Возвращаeт ответ который уйдёт пользователю.

    :param _jwt_header:
    :param jwt_data:
    :return:
    """
    return make_response(jsonify({"message": "The token has expired."}), HTTPStatus.UNAUTHORIZED)


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    Callback на случай невалидной подписи. Возвращаeт ответ который уйдёт пользователю.

    :param error:
    :return:
    """
    return make_response(jsonify({"message": "Signature verification failed."}), HTTPStatus.UNAUTHORIZED)


@jwt.revoked_token_loader
def revoked_token_callback(_jwt_header, jwt_data):
    """
    Callback на случай запроса с отозванным токеном. Возвращаeт ответ который уйдёт пользователю.

    :param _jwt_header:
    :param jwt_data:
    :return:
    """
    return make_response(jsonify({"message": "The token has been revoked."}), HTTPStatus.UNAUTHORIZED)


@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    Callback на случай отсуствия токена. Возвращаeт ответ который уйдёт пользователю.

    :param error:
    :return:
    """
    return make_response(jsonify({"message": "Request does not contain an access token."}), HTTPStatus.UNAUTHORIZED)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Callback для поиска пользователя. Нужен для корректной работы get_current_user.

    :param _jwt_header:
    :param jwt_data:
    :return:
    """
    identity = jwt_data["sub"]
    user = models.User.query.filter_by(id=identity).one_or_none()
    return user


def jwt_with_role_required(role: str):
    """
    Декоратор выполняющий функцию проверки авторизации
    За основу взят код из доки: https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/

    :return:
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if role in claims["roles"]:
                return fn(*args, **kwargs)
            else:
                return make_response(jsonify(message="you shall not pass"), HTTPStatus.FORBIDDEN)

        return decorator

    return wrapper
