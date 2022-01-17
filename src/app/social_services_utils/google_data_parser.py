from app.social_services_utils.base_data_parser import BaseDataParser
from app.social_services_utils.social_user_model import SocialUserModel


class GoogleDataParser(BaseDataParser):
    def get_user_info(self) -> SocialUserModel:
        userinfo_dict = self.client.parse_id_token(self.token)
        return SocialUserModel(
            open_id=userinfo_dict.get("sub"),
            email=userinfo_dict.get("email"),
            first_name=userinfo_dict.get("family_name"),
            last_name=userinfo_dict.get("given_name"),
        )
