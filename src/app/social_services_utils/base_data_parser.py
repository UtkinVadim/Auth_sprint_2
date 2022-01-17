from abc import ABC, abstractmethod

from app.social_services_utils.social_user_model import SocialUserModel
from authlib.integrations.flask_client import FlaskRemoteApp


class BaseDataParser(ABC):
    def __init__(self, client: FlaskRemoteApp, token):
        self.client = client
        self.token = token

    @abstractmethod
    def get_user_info(self) -> SocialUserModel:
        pass
