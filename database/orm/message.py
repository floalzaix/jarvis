#
#   Imports
#

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Perso

from database.base import Base

if TYPE_CHECKING:
    from database.orm.session import Session

#
#   Message ORM
#

class Message(Base):
    """
        Message ORM model.
    """

    __tablename__ = "messages"

    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="The role of the message OpenAI convention"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="The content of the message"
    )

    #
    #   Foreign Keys
    #

    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        doc="The session the message belongs to"
    )

    #
    #   Relationships
    #

    session: Mapped["Session"] = relationship(
        back_populates="messages"
    )