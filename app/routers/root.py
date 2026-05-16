from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from app.utils.auth import get_auth_cookie

router = APIRouter()

@router.get("/")
async def root(request: Request, cookie=Depends(get_auth_cookie)):
    if cookie is None:
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/reminders")
