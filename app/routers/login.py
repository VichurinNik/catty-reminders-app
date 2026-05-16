from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
import jwt
from app import secret_key, users
from app import templates

router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def post_login(response: Response, username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        token = jwt.encode({"username": username}, secret_key, algorithm="HS256")
        response.set_cookie(key="auth-token", value=token, httponly=True)
        return RedirectResponse(url="/reminders", status_code=303)
    else:
        return RedirectResponse(url="/login?unauthorized=True", status_code=303)
