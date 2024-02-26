from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from .asdict_mixin import AsdictMixin
from .query_mixin import QueryMixin


class Base(MappedAsDataclass, DeclarativeBase, QueryMixin, AsdictMixin):
    """Base database model"""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, init=False)
