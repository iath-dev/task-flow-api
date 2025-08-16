from app.schemas.common import TimestampBase
from app.db.models.logs import StatusEnum


class LoginLogBase(TimestampBase):
    user_id: int
    ip_address: str
    user_agent: str
    status: StatusEnum
    reason: str | None

    class Config:
        orm_mode = True
