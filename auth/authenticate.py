import logging
from auth.get_user import get_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def user( user_id: str, password: str):
    user = get_user(user_id)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        logging.error(f"Password error: {password}, user_id: {user_id}")
        return False
    return user