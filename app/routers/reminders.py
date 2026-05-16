from fastapi import APIRouter, Depends, Form, Request
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

def _get_reminders_grid(request: Request, storage: MySQLStorage):
    context = _build_full_page_context(request, storage)
    return templates.TemplateResponse("partials/reminders/content.html", context)

@router.get("/reminders", response_class=HTMLResponse)
async def get_reminders(request: Request, storage: MySQLStorage = Depends(get_storage_for_page)):
    context = _build_full_page_context(request, storage)
    return templates.TemplateResponse("pages/reminders.html", context)

@router.get("/reminders/list-row/{list_id}")
async def get_reminders_list_row(list_id: int, request: Request, storage: MySQLStorage = Depends(get_storage_for_page)):
    reminder_list = storage.get_list(list_id)
    selected_list = storage.get_selected_list()
    context = {'request': request, 'reminder_list': reminder_list, 'selected_list': selected_list}
    return templates.TemplateResponse("partials/reminders/list-row.html", context)
