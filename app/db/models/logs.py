import enum

from sqlalchemy import Column, Enum, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import IdMixin, TimestampMixin


class LogStatusEnum(str, enum.Enum):
    success = "SUCCESS"
    failed = "FAILED"


class LoginLog(IdMixin, TimestampMixin, Base):
    __tablename__ = "login_logs"

    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    status = Column(Enum(LogStatusEnum), nullable=False)
    reason = Column(String(255), nullable=True)

    user = relationship("User", back_populates="login_logs", lazy="raise")
