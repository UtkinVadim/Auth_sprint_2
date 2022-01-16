from .change_user_params import ChangeUserParams
from .refresh_token import RefreshToken
from .role import Role
from .role_manipulation import RoleManipulation
from .sign_in import SignIn
from .sign_out import SignOut
from .sign_up import SignUp
from .social_auth import SocialLogin, SocialAuth
from .start_page import Homepage
from .user_history import UserHistory
from .remove_social_account import RemoveSocialAccount

urls = [
    (SignIn, "/api/user/sign_in"),
    (SignUp, "/api/user/sign_up"),
    (SignOut, "/api/user/sign_out"),
    (RefreshToken, "/api/v1/user/refresh"),
    (ChangeUserParams, "/api/v1/user/change"),
    (UserHistory, "/api/v1/user/history"),
    (RoleManipulation, "/api/v1/user/role"),
    (Role, "/api/v1/access/role"),

    (SocialLogin, "/login/<string:name>"),
    (SocialAuth, "/api/oauth2/callback/<string:social_name>"),
    (Homepage, "/"),
    (RemoveSocialAccount, "/api/remove_social_account")
]
