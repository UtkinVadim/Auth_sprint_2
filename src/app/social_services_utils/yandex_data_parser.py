from app.social_services_utils.base_data_parser import BaseDataParser
from app.social_services_utils.social_user_model import SocialUserModel


class YandexDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        userinfo = self.client.get('https://login.yandex.ru/info?format=json')
        userinfo_dict = userinfo.json()
        return SocialUserModel(
            open_id=userinfo_dict.get("id"),
            email=userinfo_dict.get("default_email"),
            first_name=userinfo_dict.get("first_name"),
            last_name=userinfo_dict.get("last_name"),
            preffered_username=userinfo_dict.get('login')
        )
