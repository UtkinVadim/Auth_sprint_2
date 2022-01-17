from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKeyConstraint, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.models.user import User


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    user_is_active = db.Column(BOOLEAN, default=True)
    fingerprint = db.Column(db.String)
    event_date = db.Column(db.DateTime(), default=datetime.utcnow)

    __table_args__ = (ForeignKeyConstraint((user_id, user_is_active), (User.id, User.is_active)), {})

    @classmethod
    def log_sign_in(cls, user_id: str, fingerprint: str):
        """
        Создаёт запись в базе об успешном логине пользователя

        :param user_id:
        :param fingerprint:
        :return:
        """
        log = LoginHistory(fingerprint=fingerprint, user_id=user_id)
        db.session.add(log)
        db.session.commit()

    @classmethod
    def get_user_events(cls, user_id: str) -> list[dict[str, str]]:
        """
        Возвращает список успешных логонов пользователя

        :return:
        """
        events = LoginHistory.query.filter_by(user_id=user_id).order_by(LoginHistory.event_date.desc()).all()
        events_dict = [
            {"user_id": str(event.user_id), "event_date": str(event.event_date), "fingerprint": str(event.fingerprint)}
            for event in events
        ]
        return events_dict
