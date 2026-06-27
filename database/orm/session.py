#
#   Imports
#

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Perso

from database.base import Base

if TYPE_CHECKING:
    from database.orm.message import Message
    from database.orm.user import User

#
#   Session ORM
#

class Session(Base):
    """
        Session ORM model.
    """

    __tablename__ = "sessions"

    #
    #   Foreign Keys
    #
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        doc="The user who owns the session"
    )

    #
    #   Relationships
    #
    
    user: Mapped["User"] = relationship(
        back_populates="sessions"
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
