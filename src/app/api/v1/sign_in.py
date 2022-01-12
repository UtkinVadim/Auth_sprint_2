from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from app import models, redis_client

sign_in_parser = reqparse.RequestParser()
sign_in_parser.add_argument("login", dest="login", location="json", required=True, type=str, help="The user's login")
sign_in_parser.add_argument(
    "password", dest="password", type=str, location="json", required=True, help="The user's password"
)
sign_in_parser.add_argument("User-Agent", dest="fingerprint", location="headers")


class SignIn(Resource):
    """
    Класс для ручки логина пользователя.
    - параметры пользователя (логин, пароль...) находятся в args
    - с помощью args делается идентификация и аутентификация пользователя
    - если успешно, то логируется логин пользователя
    - из базы берутся роли пользователя
    - создаются access и refresh токены. В access токен кладутся роли пользователя
    - refresh токен кладётся в in-memory базу
    """

    def post(self):
        args = sign_in_parser.parse_args()
        user = models.User.check_user_by_login(args)
        if not user:
            return {"message": "invalid credentials"}, HTTPStatus.UNAUTHORIZED
        models.LoginHistory.log_sign_in(user, args["fingerprint"])
        user_roles_dict = models.User.get_user_roles(user_id=user.id)
        access_token = create_access_token(identity=user.id, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=user.id)
        redis_client.set_user_refresh_token(user_id=str(user.id), refresh_token=refresh_token)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)
