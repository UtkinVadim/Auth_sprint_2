from config import GOOGLE_DISCOVERY_URL, FACEBOOK_APP_SECRET, FACEBOOK_APP_ID


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
