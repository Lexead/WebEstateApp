from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from ..core import security
from ..db import Base


class User(Base):
    """User database model"""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str]

    @classmethod
    async def create(cls, session: AsyncSession, username: str, email: str, password: str) -> None:
        session.add(cls(username=username, email=email, password_hash=security.hash_password(password)))
        await session.commit()

    @classmethod
    async def find_by_email(cls, session: AsyncSession, email: str) -> User | None:
        query = select(cls).where(cls.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def find_by_username(cls, session: AsyncSession, username: str) -> User | None:
        query = select(cls).where(cls.username == username)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def authenticate(cls, session: AsyncSession, email: str, password: str) -> User | None:
        user = await cls.find_by_email(session, email)
        if not user or not security.verify_password(password, user.password_hash):
            return None
        return user
