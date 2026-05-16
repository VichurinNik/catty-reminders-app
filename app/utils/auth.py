import jwt
import secrets
from fastapi import Cookie, Depends
from typing import Optional
from app import db_path, users, secret_key
from app.utils.exceptions import UnauthorizedException, UnauthorizedPageException
from app.utils.storage import ReminderStorage

def serialize_token(username: str) -> str:
    return jwt.encode({"username": username}, secret_key, algorithm="HS256")

def deserialize_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload.get("username")
    except jwt.InvalidTokenError:
        return None

def get_auth_cookie(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    username = deserialize_token(auth_token)
    if username:
        return {"username": username}
    return None

def get_current_username(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    return deserialize_token(auth_token)

def get_username_for_api(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    username = deserialize_token(auth_token)
    if not username:
        raise UnauthorizedException()
    return username

def get_username_for_page(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    username = deserialize_token(auth_token)
    if not username:
        raise UnauthorizedPageException()
    return username

def get_storage_for_api(username: str = Depends(get_username_for_api)) -> ReminderStorage:
    return ReminderStorage(owner=username, db_path=db_path)

def get_storage_for_page(username: str = Depends(get_username_for_page)) -> ReminderStorage:
    return ReminderStorage(owner=username, db_path=db_path)
