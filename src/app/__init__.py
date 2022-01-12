from flask import Flask
from flask_jwt_extended import JWTManager
from app.redis_db import RedisConnector
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

import config

db = SQLAlchemy()
redis_client = RedisConnector(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
jwt = JWTManager()
swagger = Swagger(template_file='auth_api_schema.yaml')


def create_app(test_config: dict = None) -> Flask:
    """
    Функция, создающая приложение на основе переданных конфигов, либо если конфиги не переданы - приложение
    создается используя конфиги из файла config.py.
    """
    app = Flask(__name__, instance_relative_config=True)

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

    return app
