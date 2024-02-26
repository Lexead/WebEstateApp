from typing import TYPE_CHECKING, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import ColumnElement, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .declarative import Base

T = TypeVar("T", bound="Base")


class QueryMixin:
    """Mixin with simple-realized queries"""

    @classmethod
    async def all(cls: type[T], session: AsyncSession) -> Sequence[T]:
        """Get all objects from database"""

        query = select(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def get_by_id(cls: type[T], session: AsyncSession, uuid: UUID = None) -> T | None:
        """Get object from database by id"""

        if not uuid:
            return None
        return await session.get(cls, uuid)

    @classmethod
    async def filter(
        cls: type[T],
        session: AsyncSession,
        *expr: bool,
        order_by: ColumnElement[T] = None,
        descending: bool = True,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Sequence[T]:
        """Filter objects from database by expression"""

        query = select(cls).where(*expr)
        if order_by is not None:
            order = desc if descending else asc
            query = query.order_by(order(order_by))
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        result = await session.execute(query)
        return result.unique().scalars().all()

    @classmethod
    async def create(cls: type[T], session: AsyncSession, **kwargs) -> None:
        """Insert object to database"""

        kwargs = {k: v for k, v in kwargs.items() if k in cls.__table__.columns.keys()}
        session.add(cls(**kwargs))
        await session.commit()

    async def delete_instance(self: T, session: AsyncSession) -> None:
        """Delete object from database"""

        await session.delete(self)
        await session.commit()

    async def update_instance(self: T, session: AsyncSession, **kwargs) -> None:
        """Delete object from database"""
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        session.add(self)
        await session.commit()

    @classmethod
    async def count(cls: type[T], session: AsyncSession, *expr: bool) -> int:
        """Count of objects"""

        query = select(func.count()).select_from(cls).where(*expr)
        result = await session.execute(query)
        return result.unique().scalar_one()
