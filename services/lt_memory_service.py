#
#   Imports
#

from typing import List, Optional
import uuid
from ollama import Message as OllamaMessage
from email_validator import validate_email, EmailNotValidError

# Perso

from lt_database.bootstrap import get_session
from lt_database.orm.session import Session as ChatSession
from lt_database.orm.message import Message as DBMessage
from lt_database.orm.user import User as DBUser
from models.user import User as UserModel

#
#   Exceptions
#

class UserNotFoundError(Exception):
    """
        User not found error.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} not found !")

class UserAlreadyExistsError(Exception):
    """
        User already exists error.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists !")

#
#   Long Term (LT) memory service
#

class LTMemoryService: # Long Term (LT) memory service
    """
        Long Term (LT) memory service class.
    """

    def create_user(
        self,
        name: str,
        last_name: str,
        email: str,
    ) -> str:
        """
            Creates a new user saved in database. However it
            verifies tough that the user does not already exist
            using the same email. And also validates the email
            format.

            Params:
                - name: The name of the user.
                - last_name: The last name of the user.
                - email: The email of the user.

            Raises:
                - UserAlreadyExistsError: If the user already exists
                under the given email.
                - ValueError: If the email is not a valid email format.
                - DBSessionError: If there is an error when saving changes
                to the database.

            Returns:
                - The email of the created user.
        """
        
        #
        #   Validation
        #
        
        try:
            info = validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email format: {e}") from e

        email = info.email

        with get_session() as session:
            if session.query(DBUser).filter(
                DBUser.email == email
            ).first():
                raise UserAlreadyExistsError(email)

            # Creating the orm user
            user = DBUser(
                name=name,
                last_name=last_name,
                email=email
            )

            # Saving changes to the database
            session.add(user)
            session.flush()

            if not user.email:
                # In theory this should never happen, but just in case
                raise RuntimeError("User has no email !")

            return user.email

    def delete_user(
        self,
        user_email: str,
    ) -> None:
        """
            Deletes a user. It also verifies tough that the user exists.
            Then cascades the deletion of all the user's sessions and
            messages.

            Params:
                - user_email: The email of the user to delete.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given email.
                - DBSessionError: If there is an error when deleting
                the user from the database.
        """
        
        with get_session() as session:

            # Validating the user exists
            user = session.query(DBUser).filter(
                DBUser.email == user_email
            ).first()

            if not user:
                raise UserNotFoundError(user_email)

            session.query(DBUser).filter(
                DBUser.email == user_email
            ).delete()

    def create_chat_session(
        self,
        user_email: str,
    ) -> uuid.UUID:
        """
            Creates a new chat session for a user. However it
            verifies tough that the user exists using the same
            email, if not it raises a UserNotFoundError.

            Params:
                - user_email: The email of the user.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given email.
                - DBSessionError: If there is an error when saving changes
                to the database.

            Returns:
                - The id of the created chat session.
        """
        
        with get_session() as session:

            # Getting the user from the database
            user = session.query(DBUser).filter(
                DBUser.email == user_email
            ).first()
            
            # Raises the user not found error in order ot engage
            # the user creation process by the llm
            if not user:
                raise UserNotFoundError(user_email)

            # Creating the orm session
            chat_session = ChatSession(
                user_id=user.id
            )

            # Saving changes to the database
            session.add(chat_session)
            session.flush()
            session.refresh(chat_session)

            return chat_session.id

    def save_message_to_session(
        self,
        message: OllamaMessage,
        user_email: str,
        chat_session_id: Optional[uuid.UUID] = None,
    ) -> uuid.UUID:
        """
            Saves a message to a chat session. However it
            verifies tough that the user exists using the same
            email, if not it raises a UserNotFoundError. If the
            chat session is not provided, it creates a new one.

            Params:
                - message: The message to save.
                - user_email: The email of the user.
                - chat_session_id: The id of the chat session to
                save the message to.

            Returns:
                - The newly created chat session id.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given email.
                - DBSessionError: If there is an error when saving changes
                to the database.
        """

        with get_session() as session:

            # Creating the chat session if not provided
            if chat_session_id is None:
                chat_session_id = self.create_chat_session(user_email)

            # Getting the chat session from this session
            chat_session = session.query(ChatSession).filter(
                ChatSession.id == chat_session_id
            ).first()

            if not chat_session:
                # In theory this should never happen, but just in case
                raise RuntimeError("Chat session not found !")

            # Creating the ORM message
            msg = DBMessage(
                content=message.content,
                role=message.role,
                session=chat_session
            )
            
            # Saving changes to the database
            session.add(msg)
            session.flush()

            return chat_session.id

    def delete_n_previous_messages_from_session(
        self,
        session_id: uuid.UUID,
        n: int = 1,
    ) -> None:
        """
            Deletes the n previous messages from a session.

            Params:
                - session_id: The id of the session.
                - n: The number of previous messages to delete.

            Raises:
                - DBSessionError: If there is an error when deleting
                the messages from the database.
        """
        
        with get_session() as session:

            # Getting the messages from the session
            messages = session.query(DBMessage).filter(
                DBMessage.session_id == session_id
            ).order_by(DBMessage.created_at.desc()).limit(n).all()

            # Deleting the messages
            for message in messages:
                session.delete(message)
                session.flush()

            return None

    def get_user_by_name_last_name(
        self,
        name: str,
        last_name: str,
    ) -> UserModel:
        """
            Gets the email of a user by their name and last name.

            Params:
                - name: The name of the user.
                - last_name: The last name of the user.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given name and last name.

            Returns:
                - The email of the user.
        """

        with get_session() as session:
            user = session.query(DBUser).filter(
                DBUser.name == name,
                DBUser.last_name == last_name
            ).first()
            
            if not user:
                raise UserNotFoundError(f"{name} {last_name}")

            if not user.email:
                # In theory this should never happen, but just in case
                raise RuntimeError("User has no email !")

            return UserModel.model_validate(
                {
                    "name": user.name,
                    "last_name": user.last_name,
                    "email": user.email
                }
            )

    def get_user_by_email(
        self,
        email: str,
    ) -> UserModel:
        """
            Gets a user by their email.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given email.
                - DBSessionError: If there is an error when getting
                the user from the database.

            Returns:
                - The user.
        """
        
        with get_session() as session:
            user = session.query(DBUser).filter(
                DBUser.email == email
            ).first()

            if not user:
                raise UserNotFoundError(email)

            if not user.email:
                # In theory this should never happen, but just in case
                raise RuntimeError("User has no email !")

            return UserModel.model_validate(
                {
                    "name": user.name,
                    "last_name": user.last_name,
                    "email": user.email
                }
            )

    def get_messages_from_session(
        self,
        session_id: uuid.UUID,
    ) -> List[OllamaMessage]:
        """
            Gets the messages from a session.

            Params:
                - session_id: The id of the session.

            Returns:
                - The messages from the session.

            Raises:
                - DBSessionError: If there is an error when getting
                the messages from the database.
        """
        
        with get_session() as session:
            messages = session.query(DBMessage).filter(
                DBMessage.session_id == session_id
            ).all()

            return [
                OllamaMessage(
                    role=message.role,
                    content=message.content
                ) for message in messages
            ]

    def get_n_previous_session(
        self,
        user_email: str,
        n: int = 1,
    ) -> Optional[List[uuid.UUID]]:
        """
            Gets the previous session of a user.

            Params:
                - user_email: The email of the user.
                - n: The number of previous sessions to get.

            Returns:
                - The ids of the n previous sessions or
                None if the user has no previous session.

            Raises:
                - UserNotFoundError: If the user does not exist
                under the given email.
                - DBSessionError: If there is an error when getting
                the previous session from the database.
        """
        
        with get_session() as session:

            # Validating the user exists
            user = session.query(DBUser).filter(
                DBUser.email == user_email
            ).first()

            if not user:
                raise UserNotFoundError(user_email)

            # Getting the previous session
            previous_sessions = session.query(ChatSession).filter(
                ChatSession.user_id == user.id
            ).order_by(ChatSession.created_at.desc()).limit(n).all()

            if not previous_sessions:
                return None

            return [
                session.id for session in previous_sessions
            ]

    def delete_session(
        self,
        session_id: uuid.UUID,
    ) -> None:
        """
            Deletes a session.

            Params:
                - session_id: The id of the session to delete.

            Raises:
                - DBSessionError: If there is an error when deleting
                the session from the database.
        """
        
        with get_session() as session:
            session.query(ChatSession).filter(
                ChatSession.id == session_id
            ).delete()