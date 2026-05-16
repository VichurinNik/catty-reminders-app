from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app import templates, DEPLOY_REF
from app.utils.auth import get_storage_for_page
from app.utils.storage import ReminderStorage

router = APIRouter(prefix="/reminders", tags=["Pages"])

def _build_full_page_context(request: Request, storage: ReminderStorage):
    reminder_lists = storage.get_lists()
    selected_list = storage.get_selected_list()
    return {
        'request': request,
        'deploy_ref': DEPLOY_REF,
        'reminder_lists': reminder_lists,
        'selected_list': selected_list
    }

@router.get("", response_class=HTMLResponse)
async def get_reminders(request: Request, storage: ReminderStorage = Depends(get_storage_for_page)):
    context = _build_full_page_context(request, storage)
    return templates.TemplateResponse("pages/reminders.html", context)
