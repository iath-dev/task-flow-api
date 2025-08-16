import enum

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import IdMixin, TimestampMixin


class StatusEnum(str, enum.Enum):
    success = "SUCCESS"
    failed = "FAILED"


class LoginLog(IdMixin, TimestampMixin, Base):
    __tablename__ = "login_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    status = Column(Enum(StatusEnum), nullable=False)
    reason = Column(String(255), nullable=True)

    user = relationship("User", back_populates="login_logs")
