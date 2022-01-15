import datetime
import random
import string
from typing import Optional
from uuid import uuid4

from sqlalchemy import BOOLEAN, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.models.user import User


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    user_is_active = db.Column(BOOLEAN, default=True)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),
                      ForeignKeyConstraint((user_id, user_is_active),
                                           (User.id, User.is_active)),
                      {}
                      )

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'

    @classmethod
    def create_social_connect(cls, user_id, social_id, social_name, user_fields: dict[str, str] = {}):
        """
        Создаёт связку пользователь - соц сеть.
        Если пользователя в базе нет - сначала создаёт, а потом добавляет связку.

        :param user_id:
        :param social_id:
        :param social_name:
        :param user_fields:
        :return:
        """
        if not user_id:
            user_id = cls.create_user_from_social_account(**user_fields)
        if cls.is_social_exist(social_id):
            return

        social_account = SocialAccount(user_id=user_id, social_id=social_id, social_name=social_name)
        db.session.add(social_account)
        db.session.commit()
        return social_account

    @classmethod
    def create_user_from_social_account(cls,
                                        login: Optional[str] = None,
                                        password: Optional[str] = None,
                                        email: Optional[str] = '*@*',
                                        first_name: Optional[str] = None,
                                        last_name: Optional[str] = None,
                                        **kwargs
                                        ) -> str:
        """
        Создаёт нового пользователя. Метод нужен при входе через соц сети нового пользователя.

        :param login:
        :param password:
        :param email:
        :param first_name:
        :param last_name:
        :return:
        """

        if login or email:
            if user := User.get_user_by_universal_login(login=login, email=email):
                return user.id

        if not login:
            login = cls.id_generator()
        if not password:
            password = cls.id_generator()

        user = User.create({'login': login,
                            'password': password,
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name})
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def is_social_exist(cls, social_id: str) -> bool:
        """
        Проверка на существование пользователя по логину

        :param social_id:
        :return:
        """
        social_account = SocialAccount.query.filter_by(social_id=social_id).one_or_none()
        return bool(social_account)

    @staticmethod
    def id_generator(size=2, chars=string.ascii_uppercase + string.digits) -> str:
        """
        Генерирует строку,
        состоящую из радномный символ + timestamp + радномный символ (другой).
        """
        str_time = str(datetime.datetime.now().timestamp())
        return str_time.join(random.choice(chars) for _ in range(size))
