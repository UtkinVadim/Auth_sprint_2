from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource, reqparse

from app import models, redis_client


sign_out_parser = reqparse.RequestParser()
sign_out_parser.add_argument("form_all_places", type=bool, location="json", required=False)


class SignOut(Resource):
    """
    Ручка для логаута пользователя.
    - из refresh токена берётся его id
    - и удаляется из белого списка хранящегося в in-memory базе
    """

    @jwt_required(refresh=True)
    def post(self):
        args = sign_out_parser.parse_args()
        sign_out_from_all_places = args.get("form_all_places", False)
        token = get_jwt()
        if sign_out_from_all_places:
            redis_client.remove_all_user_tokens(token)
            return jsonify(message="All user tokens revoked")
        redis_client.remove_user_token(token)
        return jsonify(message="Refresh token revoked")
