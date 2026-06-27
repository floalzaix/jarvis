#
#   Imports
#

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

#
#   Base
#

class Base(DeclarativeBase):
    """
        Base class for all database ORM models.
    """

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