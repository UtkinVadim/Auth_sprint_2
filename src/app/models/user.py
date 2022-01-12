import datetime
import hashlib
from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import BOOLEAN, UUID

import config
from app import db


class User(db.Model):
    __tablename__ = "user_auth"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    roles = db.relationship("Role", secondary="user_role", backref=db.backref("user_auth", lazy="dynamic"))
    is_active = db.Column(BOOLEAN, default=True)

    @classmethod
    def create(cls, user_fields: dict) -> Optional[db.Model]:
        """
        Создаёт пользователя в базе

        :param user_fields:
        :return:
        """
        user = User(**user_fields)
        user.password = cls.password_hasher(user_fields["password"])
        if cls.is_login_exist(user_fields):
            return
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_user_by_login(cls, user_fields: dict) -> Optional[db.Model]:
        """
        Идентификация и аутентификация пользователя по логину-паролю

        :param user_fields:
        :return:
        """
        login = user_fields["login"]
        password = user_fields["password"]
        user = User.query.filter_by(login=login).one_or_none()
        if user:
            if user.password == cls.password_hasher(password):
                return user
            return
        return

    def __repr__(self):
        return f"<User {self.login} {self.id}>"

    @classmethod
    def change_user(cls, user_id: str, user_fields: dict):
        """
        Смена логина и пароля у пользователя

        :param user_id:
        :param user_fields:
        :return:
        """
        user = User.query.filter_by(id=user_id).one_or_none()
        if login := user_fields["login"]:
            user.login = login
        if password := user_fields["new_password"]:
            user.password = cls.password_hasher(password)
        db.session.commit()

    @classmethod
    def get_user_roles(cls, user_id: str) -> dict:
        """
        Возвращает словарь вида id пользователя -> список его ролей

        :param user_id:
        :return:
        """
        user = User.query.filter_by(id=user_id).one_or_none()
        roles = user.roles
        roles_list = [role.title for role in roles]
        roles_dict = {"roles": roles_list}
        return roles_dict

    @classmethod
    def is_login_exist(cls, user_fields: dict) -> bool:
        """
        Проверка на существование пользователя по логину

        :param user_fields:
        :return:
        """
        login = user_fields["login"]
        user = User.query.filter_by(login=login).one_or_none()
        if user:
            return True
        return False

    @classmethod
    def password_hasher(
            cls, password: str, salt: str = config.SALT, hash_name: str = "sha256", iterations: int = 100000,
            encoding: str = "utf-8"
    ) -> str:
        """
        Создаёт хэш от пароля который будет храниться в базе
        дока: https://docs.python.org/3.9/library/hashlib.html#hashlib.pbkdf2_hmac

        :param password:
        :param salt:
        :param hash_name:
        :param iterations:
        :param encoding:
        :return:
        """
        password_salted_hash = hashlib.pbkdf2_hmac(
            hash_name, password.encode(encoding), salt.encode(encoding), iterations
        ).hex()
        return password_salted_hash

    def check_password(self, password: str) -> bool:
        return self.password == self.password_hasher(password)
