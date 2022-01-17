from abc import ABC, abstractmethod

from authlib.oauth2.rfc6749.wrappers import OAuth2Token
from authlib.integrations.flask_client import FlaskRemoteApp
from app.social_services_utils.social_user_model import SocialUserModel


class BaseDataParser(ABC):
    def __init__(self, client: FlaskRemoteApp, token: OAuth2Token):
        self.client = client
        self.token = token

    @abstractmethod
    def get_user_info(self) -> SocialUserModel:
        pass
