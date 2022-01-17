from flasgger import Swagger
from flask import Flask, request, Blueprint
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import config
from app.telemetry import add_tracer
from app.redis_db import RedisConnector
from app.social_services_utils.oauth_services import create_oauth_services

db = SQLAlchemy()
redis_client = RedisConnector(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
jwt = JWTManager()
swagger = Swagger(template_file='auth_api_schema.yaml')
oauth = OAuth()
limiter = Limiter(key_func=get_remote_address, storage_uri=config.BUCKET_REDIS_URI, default_limits=["30 per minute"])

core_api_bp = Blueprint('core_api', __name__)
api_v1_bp = Blueprint('api_v1', __name__)


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
        add_tracer(app)
        if config.USE_NGINX:
            @app.before_request
            def before_request():
                """
                Добавляет строгую проверку наличия заголовка 'X-Request-Id'
                Если заголовка нет - возбуждает исключение

                :return:
                """
                request_id = request.headers.get('X-Request-Id')
                if not request_id:
                    raise RuntimeError('request id is required')
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    # подключение постоянных ручек
    api = Api(core_api_bp)
    from app.api.urls import api_urls
    for resource, url in api_urls:
        api.add_resource(resource, url)
    app.register_blueprint(core_api_bp, url_prefix='/')

    # подключение версионных ручек
    api_v1 = Api(api_v1_bp)
    from app.api.v1.urls import api_v1_urls
    for resource, url in api_v1_urls:
        api_v1.add_resource(resource, url)
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    swagger.init_app(app)

    oauth.init_app(app)
    create_oauth_services(oauth)

    limiter.init_app(app)
    print(app.url_map)

    return app
