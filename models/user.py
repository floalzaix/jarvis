#
#   Imports
#

from pydantic import BaseModel, Field

#
#   User Model
#

class User(BaseModel):
    """
        User model.
    """
    name: str = Field(..., description="The first name of the user")
    last_name: str = Field(..., description="The last name of the user")
    email: str = Field(..., description="The email of the user")