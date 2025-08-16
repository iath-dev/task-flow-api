import enum

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.db.mixins import IdMixin, TimestampMixin


class UserStatusEnum(str, enum.Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
    pending = "PENDING"
    suspended = "SUSPENDED"
    deleted = "DELETED"


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    full_name = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.active)

    last_access = Column(DateTime, default=func.now(), onupdate=func.now())

    login_logs = relationship("LoginLog", back_populates="user", lazy="raise")
