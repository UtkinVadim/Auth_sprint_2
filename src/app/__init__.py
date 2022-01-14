from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import config
from app.social_services_utils.oauth_services import google_register, facebook_register
from app.redis_db import RedisConnector

db = SQLAlchemy()
redis_client = RedisConnector(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
jwt = JWTManager()
swagger = Swagger(template_file='auth_api_schema.yaml')
oauth = OAuth()
limiter = Limiter(key_func=get_remote_address, storage_uri=config.BUCKET_REDIS_URI, default_limits=["30 per minute"])


def create_app(test_config: dict = None) -> Flask:
    """
    Функция, создающая приложение на основе переданных конфигов, либо если конфиги не переданы - приложение
    создается используя конфиги из файла config.py.
    """
    app = Flask(__name__, instance_relative_config=True, template_folder="../templates")

    app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_TRACK_MODIFICATIONS=False)

    if test_config is None:
        app.config.from_object("config")
        jwt.init_app(app)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    api = Api(app)
    from app.api.v1.urls import urls

    for resource, url in urls:
        api.add_resource(resource, url)

    swagger.init_app(app)

    oauth.init_app(app)
    google_register(oauth)
    facebook_register(oauth)

    limiter.init_app(app)

    return app
