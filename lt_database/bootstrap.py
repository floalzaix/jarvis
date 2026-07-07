#
#   Imports
#

import streamlit as st

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text

# Personal

from config.config import get_settings, Env

settings = get_settings()

#
#   Exceptions
#

class DBSessionError(Exception):
    """
        If there is an error when saving changes to the database
        and it is caused by the access to the database or the
        db itself.
    """

    def __init__(self, sub_error: Exception):
        self.sub_error = sub_error
        super().__init__("Error when saving changes "
        f"to the database: {sub_error}")

#
#   Bootstrap
#

settings = get_settings()

@st.cache_resource
def bootstrap_db() -> sessionmaker[Session]:
    """
        Bootstrap the database by setting up the engine and the session maker.
    """

    URL = settings.LT_MEMORY_DATABASE_URL

    # Creating the engine
    engine: Engine = create_engine(
        URL,
        echo=False,
    )

    # Creating the session maker
    _session_maker = sessionmaker[Session](
        engine,
        expire_on_commit=False,
    )

    # Trying peremissions and at least one table exists
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        raise RuntimeError(
            "Error verifying permissions or table existence. "
            "Please check your database configuration. \n"
            f"Error: {e}"
        ) from e

    return _session_maker

@contextmanager
def get_session() -> Generator[Session, None]:
    """
        Get a session from the session maker.
    """
    session_maker = bootstrap_db()

    session = session_maker()
    
    try:
        yield session
        session.commit()

    except Exception as e:
        session.rollback()
        raise DBSessionError(e) from e

    finally:
        session.close()
