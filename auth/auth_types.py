from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class TokenData(BaseModel):
    username: Optional[str] = None