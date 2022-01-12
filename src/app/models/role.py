from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app import db


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}"

    @classmethod
    def get_all(cls) -> list[dict[str, str]]:
        """
        Возвращает полный список ролей

        :return:
        """
        roles = cls.query.all()
        roles_dict = [{"id": str(role.id), "title": str(role.title)} for role in roles]
        return roles_dict

    @classmethod
    def is_role_exist(cls, role_fields: dict) -> bool:
        """
        Проверка на существование роли

        :param role_fields:
        :return:
        """
        title = role_fields["title"]
        role = Role.query.filter_by(title=title).one_or_none()
        if role:
            return True
        return False

    @classmethod
    def create(cls, **role_fields) -> db.Model:
        """
        Создаёт новую роль

        :param role_fields:
        :return:
        """
        role = Role(**role_fields)
        db.session.add(role)
        db.session.commit()
        return role

    @classmethod
    def delete(cls, role):
        """
        Удаляет роль

        :param role:
        :return:
        """
        db.session.delete(role)
        db.session.commit()

    @classmethod
    def update(cls, role_fields: dict):
        """
        Обновление информации о роли

        :param role_fields:
        :return:
        """
        current_title = role_fields["title"]
        role = Role.query.filter_by(title=current_title).one_or_none()
        role.title = role_fields["new_title"]
        db.session.commit()
