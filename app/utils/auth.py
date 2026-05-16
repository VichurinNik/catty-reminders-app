import jwt
import secrets
from app import db_config, users, secret_key
from app.utils.exceptions import UnauthorizedException, UnauthorizedPageException
from app.utils.mysql_storage import MySQLStorage
from fastapi import Cookie, Depends, Form
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from typing import Optional

class AuthCookie(BaseModel):
    username: str

def verify_password(username: str, password: str) -> bool:
    return users.get(username) == password

def serialize_token(username: str) -> str:
    return jwt.encode({"username": username}, secret_key, algorithm="HS256")

def deserialize_token(token: str) -> Optional[AuthCookie]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return AuthCookie(username=payload["username"])
    except jwt.InvalidTokenError:
        return None

def get_auth_cookie(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    return deserialize_token(auth_token)

def get_username_for_api(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    cookie = deserialize_token(auth_token)
    if not cookie:
        raise UnauthorizedException()
    return cookie.username

def get_username_for_page(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    cookie = deserialize_token(auth_token)
    if not cookie:
        raise UnauthorizedPageException()
    return cookie.username

def get_storage_for_api(username: str = Depends(get_username_for_api)) -> MySQLStorage:
    return MySQLStorage(owner=username, db_config=db_config)

def get_storage_for_page(username: str = Depends(get_username_for_page)) -> MySQLStorage:
    return MySQLStorage(owner=username, db_config=db_config)
