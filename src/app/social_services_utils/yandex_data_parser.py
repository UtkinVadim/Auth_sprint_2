from app.social_services_utils.base_data_parser import BaseDataParser
from app.social_services_utils.social_user_model import SocialUserModel
from config import YANDEX_USERINFO_URL


class YandexDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        userinfo = self.client.get(YANDEX_USERINFO_URL)
        userinfo_dict = userinfo.json()
        return SocialUserModel(
            open_id=userinfo_dict.get("id"),
            email=userinfo_dict.get("default_email"),
            first_name=userinfo_dict.get("first_name"),
            last_name=userinfo_dict.get("last_name"),
            preffered_username=userinfo_dict.get('login')
        )
