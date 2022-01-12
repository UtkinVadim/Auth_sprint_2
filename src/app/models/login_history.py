from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app import db


class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user_auth.id"), nullable=False)
    fingerprint = db.Column(db.String)
    event_date = db.Column(db.DateTime(), default=datetime.utcnow)

    @classmethod
    def log_sign_in(cls, user, fingerprint):
        """
        Создаёт запись в базе об успешном логине пользователя

        :param user:
        :param fingerprint:
        :return:
        """
        log = LoginHistory(fingerprint=fingerprint, user_id=user.id)
        db.session.add(log)
        db.session.commit()

    @classmethod
    def get_user_events(cls, user_id) -> list[dict[str, str]]:
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
