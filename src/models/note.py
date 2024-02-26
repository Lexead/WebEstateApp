from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base, utcnow
from .user import User


class Note(Base):
    """Note database model"""

    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

    @classmethod
    async def find_by_user(cls, session: AsyncSession, user: User | UUID = None):
        if not user:
            return []
        user_id = user.id if isinstance(user, User) else user
        query = select(cls).where(cls.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
