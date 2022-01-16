from http import HTTPStatus
from typing import Type

import config
from app import models, oauth, redis_client
from app.social_services_utils import (BaseDataParser, FacebookDataParser,
                                       GoogleDataParser, YandexDataParser,
                                       VkDataParser)
from authlib.integrations.flask_client import FlaskRemoteApp
from flask import jsonify, make_response, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

sign_in_parser = reqparse.RequestParser()
sign_in_parser.add_argument("User-Agent", dest="fingerprint", location="headers")


class SocialLogin(Resource):
    """
    Класс логина в соц сети, на вход принимает имя соцсети, после чего устремляется по спец урлу этой соцсети
    в рамках выполнения протокола oauth. В случае успеха будет редирект на класс авторизации через соцсеть.
    Пользователь видит окно соцсети с запросом предоставления доступа именно в результате работы этого класса.
    """
    def get(self, name):
        client = oauth.create_client(name)
        if not client:
            return {"message": "invalid social service"}, HTTPStatus.UNAUTHORIZED

        # PREFERRED_URL_SCHEME из env почему то игнорируется, поэтому явно указываю _scheme
        if config.USE_NGINX:
            scheme = 'https'
        else:
            scheme = 'http'
        redirect_uri = url_for('socialauth', social_name=name, _external=True, _scheme=scheme)
        return client.authorize_redirect(redirect_uri)


class SocialAuth(Resource):
    """
    Класс авторизации через соцсеть. На вход принимает имя соцсети.
    Проходит авторизацию в соцсети, получает данные о пользователе,
    по этим данным как на кофейной гуще гадает - есть ли у нас этот пользователь в базе
    (гадание начинается в models.SocialAccount.create_social_connect и дальше по коду)
    Не нашли пользователя - создаём себе нового, нашли - не создаём
    Добавляем привязку соцсети к пользователю (опять же если её не было)

    И в самом конце уже как обычно логируем заход пользователя и возвращаем уже наши access и refresh jwt
    """
    def get(self, social_name):
        # FIXME имхо, функция получлась "жирная" и запутанная.
        #  Первый кандидат на разбивку после добавления всех авторизация
        args = sign_in_parser.parse_args()
        client: FlaskRemoteApp = oauth.create_client(social_name)
        if not client:
            return {"message": "invalid social service"}, HTTPStatus.UNAUTHORIZED
        token = client.authorize_access_token()

        user_data_parser = self.get_user_data_parser(client.name)
        user_data = user_data_parser(client, token).get_user_info()

        # если social_id нет в базе - создать
        if not models.SocialAccount.is_social_exist(user_data.open_id):
            models.SocialAccount.create_social_connect(user_id=None,
                                                       social_id=user_data.open_id,
                                                       social_name=social_name,
                                                       user_fields=user_data.dict())

        user_id = models.SocialAccount.query.filter_by(social_id=user_data.open_id).first().user_id

        # обычная процедура логирования логина и выдачи jwt
        models.LoginHistory.log_sign_in(user_id, args["fingerprint"])
        user_roles_dict = models.User.get_user_roles(user_id=user_id)
        access_token = create_access_token(identity=user_id, additional_claims=user_roles_dict)
        refresh_token = create_refresh_token(identity=user_id)
        redis_client.set_user_refresh_token(user_id=str(user_id), refresh_token=refresh_token)
        return make_response(jsonify(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK)

    def get_user_data_parser(self, client_name: str) -> Type[BaseDataParser]:
        parsers = {
            "facebook": FacebookDataParser,
            "yandex": YandexDataParser,
            "google": GoogleDataParser,
            "vk": VkDataParser
        }
        return parsers[client_name]
