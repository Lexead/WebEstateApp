from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base, utcnow


class BlackListToken(Base):
    __tablename__ = "blacklist_tokens"

    expire: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
