import jwt
import secrets
from fastapi import Cookie, Depends, HTTPException
from fastapi.security import HTTPBasic
from typing import Optional
from app import db_config, users, secret_key
from app.utils.mysql_storage import MySQLStorage

def get_current_username(auth_token: Optional[str] = Cookie(None, alias="auth-token")):
    if auth_token is None:
        return None
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
        return payload.get("username")
    except jwt.InvalidTokenError:
        return None

def get_storage_for_api(username: str = Depends(get_current_username)):
    if username is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return MySQLStorage(owner=username, db_config=db_config)

def get_storage_for_page(username: str = Depends(get_current_username)):
    if username is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return MySQLStorage(owner=username, db_config=db_config)
