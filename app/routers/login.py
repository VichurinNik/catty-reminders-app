from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from app import templates, DEPLOY_REF
from app.utils.auth import serialize_token, get_auth_cookie
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter()

@router.get("/login")
async def get_login(request: Request, invalid: bool = False, logged_out: bool = False, unauthorized: bool = False):
    return templates.TemplateResponse("pages/login.html", {
        "request": request,
        "deploy_ref": DEPLOY_REF,
        "invalid": invalid,
        "logged_out": logged_out,
        "unauthorized": unauthorized
    })

@router.post("/login")
async def post_login(response: Response, username: str = Form(...), password: str = Form(...)):
    from app import users
    if users.get(username) == password:
        token = serialize_token(username)
        response.set_cookie(key="auth-token", value=token, httponly=True)
        return RedirectResponse(url="/reminders", status_code=303)
    else:
        return RedirectResponse(url="/login?invalid=True", status_code=303)

@router.get("/logout")
@router.post("/logout")
async def logout(response: Response, cookie=Depends(get_auth_cookie)):
    if not cookie:
        raise UnauthorizedPageException()
    response = RedirectResponse(url="/login?logged_out=True", status_code=303)
    response.set_cookie(key="auth-token", value="", expires=-1)
    return response
