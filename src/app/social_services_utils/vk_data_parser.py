from app.social_services_utils import BaseDataParser

from app.social_services_utils.social_user_model import SocialUserModel


class VkDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        user_info_url = f"https://api.vk.com/method/users.get?v=5.131"
        response = self.client.get(user_info_url)
        userinfo_dict = response.json()["response"][0]
        return SocialUserModel(
            open_id=userinfo_dict.get("id"),
            email=self.token.get("email"),
            first_name=userinfo_dict.get("first_name"),
            last_name=userinfo_dict.get("last_name")
        )
