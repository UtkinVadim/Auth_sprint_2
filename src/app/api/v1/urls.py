from .change_user_params import ChangeUserParams
from .refresh_token import RefreshToken
from .role import Role
from .role_manipulation import RoleManipulation
from .sign_in import SignIn
from .sign_out import SignOut
from .sign_up import SignUp
from .user_history import UserHistory

urls = [
    (SignIn, "/api/user/sign_in"),
    (SignUp, "/api/user/sign_up"),
    (SignOut, "/api/user/sign_out"),
    (RefreshToken, "/api/v1/user/refresh"),
    (ChangeUserParams, "/api/v1/user/change"),
    (UserHistory, "/api/v1/user/history"),
    (RoleManipulation, "/api/v1/user/role"),
    (Role, "/api/v1/access/role"),
]