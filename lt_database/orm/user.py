#
#   Imports
#

from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Perso

from lt_database.base import Base

if TYPE_CHECKING:
    from lt_database.orm.session import Session

#
#   User ORM
#

class User(Base):
    """
        User ORM model.
    """

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="The first name of the user"
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="The last name of the user"
    )

    email: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=False,
        doc="The email address of the user"
    )

    #
    #   Relationships
    #
    
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    #
    #   Constraints
    #
    
    __table_args__ = (
        UniqueConstraint("name", "last_name", name="unique_name_last_name"),
    )
