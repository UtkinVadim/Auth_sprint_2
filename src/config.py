import datetime
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=False))

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
schema_name = "public"
SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"options": f"-csearch_path={schema_name}"}}

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 5)))
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 15)))
PROPAGATE_EXCEPTIONS = True

SALT = os.getenv("SALT")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
REDIS_DB = int(os.getenv("REDIS_DB", 0))

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))

TEST_DB = os.getenv("TEST_DB")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")

TEST_REDIS_HOST = os.getenv("TEST_REDIS_HOST")
TEST_REDIS_PORT = int(os.getenv("TEST_REDIS_PORT"))
TEST_REDIS_DB = int(os.getenv("TEST_REDIS_DB", 0))

SUPERUSER_NAME = os.getenv("SUPERUSER_NAME")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")
SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL")

FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")
FACEBOOK_USERINFO_URL = "https://graph.facebook.com/me?fields=id,name,email{url}"
FACEBOOK_API_BASE_URL = "https://graph.facebook.com/"
FACEBOOK_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
FACEBOOK_AUTHORIZE_URL = "https://www.facebook.com/dialog/oauth"
FACEBOOK_OAUTH_SETTINGS = {"scope": "email openid public_profile"}

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = os.getenv("GOOGLE_DISCOVERY_URL")
GOOGLE_OAUTH_SETTINGS = {"scope": "openid email profile"}

YANDEX_APP_ID = os.getenv("YANDEX_APP_ID")
YANDEX_APP_SECRET = os.getenv("YANDEX_APP_SECRET")
YANDEX_API_BASE_URL = "https://login.yandex.ru/"
YANDEX_ACCESS_TOKEN_URL = "https://oauth.yandex.com/token"
YANDEX_AUTHORIZE_URL = "https://oauth.yandex.com/authorize"
YANDEX_USERINFO_URL = "https://login.yandex.ru/info?format=json"

VK_CLIENT_ID = os.getenv("VK_CLIENT_ID")
VK_SECRET_KEY = os.getenv("VK_SECRET_KEY")
VK_API_BASE_URL = "https://api.vk.com/method/"
VK_ACCESS_TOKEN_URL = "https://oauth.vk.com/access_token"
VK_AUTHORIZE_URL = "https://oauth.vk.com/authorize"
VK_USERINFO_URL = "https://api.vk.com/method/users.get?v=5.131"
VK_OAUTH_SETTINGS = {
    "token_placement": "uri",
    "token_endpoint_auth_method": "client_secret_post",
    "scope": "email"
}

BUCKET_REDIS_DATABASE = 1
BUCKET_REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}?db={BUCKET_REDIS_DATABASE}"

USE_NGINX = int(os.getenv("USE_NGINX", 0))

JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")
JAEGER_PORT = int(os.getenv("JAEGER_PORT", 6831))
SERVICE_NAME_IN_JAEGER = '_'.join(["movies", SERVER_HOST, POSTGRES_HOST, REDIS_HOST])
JAEGER_EXCLUDED_URLS = os.getenv("JAEGER_EXCLUDED_URLS", "")
