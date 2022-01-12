import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from app import db


class UserRole(db.Model):
    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="unique_user_role"),)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user_auth.id"), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("role.id"), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    @classmethod
    def add(cls, user_id, role_id):
        """
        Добавляет роль пользователю

        :param user_id:
        :param role_id:
        :return:
        """
        user_role = UserRole(user_id=user_id, role_id=role_id)
        db.session.add(user_role)
        db.session.commit()

    @classmethod
    def delete(cls, user_id, role_id):
        """
        Удаляет роль у пользователя

        :param user_id:
        :param role_id:
        :return:
        """
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).one_or_none()
        db.session.delete(user_role)
        db.session.commit()

    @classmethod
    def is_user_role_exists(cls, user_fields: dict) -> bool:
        """
        Проверка на существование пользователя по логину

        :param user_fields:
        :return:
        """
        user_id = user_fields["user_id"]
        role_id = user_fields["role_id"]
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).one_or_none()
        if user_role:
            return True
        return False
