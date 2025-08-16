from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func


class IdMixin:
    """
    Mixin for models that require an auto-increment integer ID.
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class TimestampMixin:
    """
    Mixin for models that require created_at and updated_at timestamps.
    """

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
