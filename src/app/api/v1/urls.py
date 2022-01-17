from .change_user_params import ChangeUserParams
from .refresh_token import RefreshToken
from .role import Role
from .role_manipulation import RoleManipulation
from .user_history import UserHistory


api_v1_urls = [
    (RefreshToken, "/user/refresh"),
    (ChangeUserParams, "/user/change"),
    (UserHistory, "/user/history"),
    (RoleManipulation, "/user/role"),
    (Role, "/access/role"),
]
