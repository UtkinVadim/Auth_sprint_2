from app.social_services_utils.base_data_parser import BaseDataParser
from app.social_services_utils.social_user_model import SocialUserModel
from config import FACEBOOK_USERINFO_URL


class FacebookDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        userinfo = self.client.get(FACEBOOK_USERINFO_URL)
        userinfo_dict = userinfo.json()
        return SocialUserModel(
            open_id=userinfo_dict.get("id"),
            email=userinfo_dict.get("email"),
            first_name=userinfo_dict.get("name").split(" ")[0],
            last_name=userinfo_dict.get("name").split(" ")[1],
        )
