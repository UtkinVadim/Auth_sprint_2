from flask import session, make_response
from flask_restful import Resource


class Homepage(Resource):
    """
    Класс для отрисовки примитивной страницы входа, облегчает тестирование.
    Убрать как всё заработает.
    """

    def get(self):
        user = session.get('user')
        return make_response(f'''<html>
                                 <a href="/login/google">google login</a>
                                 <br/>
                                 {user}
                                 </html>''')
