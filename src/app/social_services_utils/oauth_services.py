from enum import Enum

from authlib.integrations.flask_client.oauth_registry import OAuth

from config import (
    FACEBOOK_ACCESS_TOKEN_URL,
    FACEBOOK_API_BASE_URL,
    FACEBOOK_APP_ID,
    FACEBOOK_APP_SECRET,
    FACEBOOK_AUTHORIZE_URL,
    FACEBOOK_OAUTH_SETTINGS,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_DISCOVERY_URL,
    GOOGLE_OAUTH_SETTINGS,
    VK_ACCESS_TOKEN_URL,
    VK_API_BASE_URL,
    VK_AUTHORIZE_URL,
    VK_CLIENT_ID,
    VK_OAUTH_SETTINGS,
    VK_SECRET_KEY,
    YANDEX_ACCESS_TOKEN_URL,
    YANDEX_API_BASE_URL,
    YANDEX_APP_ID,
    YANDEX_APP_SECRET,
    YANDEX_AUTHORIZE_URL,
)


class Services(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    YANDEX = "yandex"
    VK = "vk"


def google_register(oauth: OAuth) -> None:
    """
    Регистрирует гугл как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name=Services.GOOGLE.value,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=GOOGLE_DISCOVERY_URL,
        client_kwargs=GOOGLE_OAUTH_SETTINGS,
    )


def facebook_register(oauth: OAuth) -> None:
    """
    Регистрирует facebook как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name=Services.FACEBOOK.value,
        client_id=FACEBOOK_APP_ID,
        client_secret=FACEBOOK_APP_SECRET,
        api_base_url=FACEBOOK_API_BASE_URL,
        access_token_url=FACEBOOK_ACCESS_TOKEN_URL,
        authorize_url=FACEBOOK_AUTHORIZE_URL,
        access_token_params=None,
        authorize_params=None,
        client_kwargs=FACEBOOK_OAUTH_SETTINGS,
    )


def yandex_register(oauth: OAuth) -> None:
    """
    Регистрирует yandex как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name=Services.YANDEX.value,
        client_id=YANDEX_APP_ID,
        client_secret=YANDEX_APP_SECRET,
        api_base_url=YANDEX_API_BASE_URL,
        access_token_url=YANDEX_ACCESS_TOKEN_URL,
        authorize_url=YANDEX_AUTHORIZE_URL,
    )


def vk_register(oauth: OAuth) -> None:
    """
    Регистрирует vkontakte как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name=Services.VK.value,
        client_id=VK_CLIENT_ID,
        client_secret=VK_SECRET_KEY,
        api_base_url=VK_API_BASE_URL,
        access_token_url=VK_ACCESS_TOKEN_URL,
        authorize_url=VK_AUTHORIZE_URL,
        client_kwargs=VK_OAUTH_SETTINGS,
    )


def create_oauth_services(oauth: OAuth) -> None:
    google_register(oauth)
    facebook_register(oauth)
    yandex_register(oauth)
    vk_register(oauth)
