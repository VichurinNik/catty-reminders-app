from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.utils.auth import get_auth_cookie

router = APIRouter()

@router.get("/")
async def root(cookie=Depends(get_auth_cookie)):
    return RedirectResponse(url="/reminders" if cookie else "/login")
