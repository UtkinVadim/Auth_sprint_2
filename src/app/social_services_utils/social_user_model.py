from pydantic import BaseModel


class SocialUserModel(BaseModel):
    open_id: str = None
    email: str = None
    first_name: str = None
    last_name: str = None
