from config import (
    GOOGLE_DISCOVERY_URL,
    FACEBOOK_APP_SECRET,
    FACEBOOK_APP_ID,
    YANDEX_APP_SECRET,
    YANDEX_APP_ID,
    VK_CLIENT_ID,
    VK_SECRET_KEY
)


def google_register(oauth):
    """
    Регистрирует гугл как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name='google',
        server_metadata_url=GOOGLE_DISCOVERY_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


def facebook_register(oauth):
    """
    Регистрирует facebook как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_APP_ID,
        client_secret=FACEBOOK_APP_SECRET,
        access_token_url="https://graph.facebook.com/oauth/access_token",
        access_token_params=None,
        authorize_url="https://www.facebook.com/dialog/oauth",
        authorize_params=None,
        api_base_url="https://graph.facebook.com/",
        client_kwargs={"scope": "email openid public_profile"}
    )


def yandex_register(oauth):
    """
    Регистрирует yandex как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name='yandex',
        client_id=YANDEX_APP_ID,
        client_secret=YANDEX_APP_SECRET,
        api_base_url='https://login.yandex.ru/',
        access_token_url='https://oauth.yandex.com/token',
        authorize_url='https://oauth.yandex.com/authorize',
    )


def vk_register(oauth):
    """
    Регистрирует vkontakte как сервис в котором можно пройти oauth
    После регистрации oauth получает атрибут с именем указанным в name

    :param oauth:
    :return:
    """
    oauth.register(
        name='vk',
        client_id=VK_CLIENT_ID,
        client_secret=VK_SECRET_KEY,
        api_base_url="https://api.vk.com/method/",
        access_token_url="https://oauth.vk.com/access_token",
        authorize_url="https://oauth.vk.com/authorize",
        client_kwargs={
            "token_placement": "uri",
            "token_endpoint_auth_method": "client_secret_post",
            "scope": "email"
        }
    )


def create_oauth_services(oauth):
    google_register(oauth)
    facebook_register(oauth)
    yandex_register(oauth)
    vk_register(oauth)
