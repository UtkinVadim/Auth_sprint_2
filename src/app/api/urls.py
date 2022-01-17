from .remove_social_account import RemoveSocialAccount
from .sign_in import SignIn
from .sign_out import SignOut
from .sign_up import SignUp
from .social_auth import SocialAuth, SocialLogin
from .start_page import Homepage


api_urls = [
    (SignIn, "/api/user/sign_in"),
    (SignUp, "/api/user/sign_up"),
    (SignOut, "/api/user/sign_out"),
    (SocialLogin, "/login/<string:name>"),
    (SocialAuth, "/api/oauth2/callback/<string:social_name>"),
    (RemoveSocialAccount, "/api/remove_social_account"),
    (Homepage, "/"),
]
