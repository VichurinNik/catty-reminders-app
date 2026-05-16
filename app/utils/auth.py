import jwt
import secrets
from fastapi import Cookie, Depends, HTTPException
from typing import Optional
from app import db_config, users, secret_key
from app.utils.mysql_storage import MySQLStorage

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

def get_storage_for_api(username: str = Depends(get_current_username)):
    if username is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return MySQLStorage(owner=username, db_config=db_config)

def get_storage_for_page(username: str = Depends(get_current_username)):
    if username is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return MySQLStorage(owner=username, db_config=db_config)
