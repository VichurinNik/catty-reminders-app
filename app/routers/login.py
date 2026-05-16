from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from app import templates, users, secret_key
from app.utils.auth import serialize_token
import jwt

router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def post_login(response: Response, username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        token = serialize_token(username)
        response.set_cookie(key="auth-token", value=token, httponly=True)
        return RedirectResponse(url="/reminders", status_code=303)
    else:
        return RedirectResponse(url="/login?unauthorized=True", status_code=303)
