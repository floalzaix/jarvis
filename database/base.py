#
#   Imports
#

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Uuid, func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#
#   Base
#

convention = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """
        Base class for all database ORM models.
    """

    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column( # type: ignore
        Uuid(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
        doc="The unique UUID identifier of the record"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )