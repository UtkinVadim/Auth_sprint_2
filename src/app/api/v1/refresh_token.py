from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_restful import Resource

from app import models, redis_client


class RefreshToken(Resource):
    """
    Класс для ручки обновления refresh токена
    - из токена берутся identity (id пользователя) и old_jti (id текущего refresh токена)
    - из in-memory базы удаляется из белого списка refresh токен
    - по identity собираются актуальные роли пользователя
    - формируется access токен, куда также кладутся роли пользователя и refresh токен
    - refresh токен кладётся в in-momory базу
    - пользователю возвращается пара access и refresh токенов
    """

    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        user_roles_dict = models.User.get_user_roles(user_id=user_id)
        access_token = create_access_token(identity=user_id, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=user_id)
        old_jwt = get_jwt()
        redis_client.refresh_user_token(str(user_id), old_jwt, access_token)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)
