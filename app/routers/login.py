from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from app.utils.auth import serialize_token, verify_password
from app import templates

router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def post_login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    if verify_password(username, password):
        token = serialize_token(username)
        response.set_cookie(key="auth-token", value=token)
        return RedirectResponse(url="/reminders", status_code=303)
    else:
        return templates.TemplateResponse("pages/login.html", {"request": {}}, status_code=401)
