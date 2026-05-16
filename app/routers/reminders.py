from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app import templates
from app.utils.auth import get_storage_for_page
from app.utils.mysql_storage import MySQLStorage

router = APIRouter()

def _build_full_page_context(request: Request, storage: MySQLStorage):
    reminder_lists = storage.get_lists()
    selected_list = storage.get_selected_list()
    return {
        'request': request,
        'reminder_lists': reminder_lists,
        'selected_list': selected_list
    }

@router.get("/reminders", response_class=HTMLResponse)
async def get_reminders(request: Request, storage: MySQLStorage = Depends(get_storage_for_page)):
    context = _build_full_page_context(request, storage)
    return templates.TemplateResponse("pages/reminders.html", context)
