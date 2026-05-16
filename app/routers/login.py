from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from app.utils.auth import AuthCookie, get_login_form_creds, get_auth_cookie, serialize_token, verify_password
from app import templates

router = APIRouter()

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})

@router.post("/login")
async def post_login(response: Response, creds = Depends(get_login_form_creds)):
    if verify_password(creds.username, creds.password):
        token = serialize_token(creds.username)
        cookie = AuthCookie(name="auth-token", token=token)
        response.set_cookie(key=cookie.name, value=cookie.token)
        return RedirectResponse(url="/reminders", status_code=303)
    else:
        return templates.TemplateResponse("pages/login.html", {"request": creds}, status_code=401)
