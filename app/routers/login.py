from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import RedirectResponse
from app import templates
from app import get_deploy_ref
from app.utils.auth import AuthCookie, get_login_form_creds, get_auth_cookie
from app.utils.exceptions import UnauthorizedPageException

router = APIRouter()

@router.get("/login")
async def get_login(request: Request, invalid: bool = False, logged_out: bool = False, unauthorized: bool = False):
    context = {
        'request': request,
        'deploy_ref': get_deploy_ref(),
        'invalid': invalid,
        'logged_out': logged_out,
        'unauthorized': unauthorized
    }
    return templates.TemplateResponse("pages/login.html", context)

@router.post("/login")
async def post_login(cookie: Optional[AuthCookie] = Depends(get_login_form_creds)) -> dict:
    if cookie:
        response = RedirectResponse('/reminders', status_code=302)
        response.set_cookie(key=cookie.name, value=cookie.token)
    else:
        response = RedirectResponse('/login?invalid=True', status_code=302)
    return response

@router.get("/logout")
@router.post("/logout")
async def logout(cookie: Optional[AuthCookie] = Depends(get_auth_cookie)) -> dict:
    if not cookie:
        raise UnauthorizedPageException()
    response = RedirectResponse('/login?logged_out=True', status_code=302)
    response.set_cookie(key=cookie.name, value=cookie.token, expires=-1)
    return response
