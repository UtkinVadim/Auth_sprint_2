from app.social_services_utils.base_data_parser import BaseDataParser
from app.social_services_utils.social_user_model import SocialUserModel
from config import VK_USERINFO_URL


class VkDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        response = self.client.get(VK_USERINFO_URL)
        userinfo_dict = response.json()["response"][0]
        return SocialUserModel(
            open_id=userinfo_dict.get("id"),
            email=self.token.get("email"),
            first_name=userinfo_dict.get("first_name"),
            last_name=userinfo_dict.get("last_name")
        )
