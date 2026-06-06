from collections.abc import Callable

from fastapi import APIRouter, Depends

from core.i18n import get_language, get_translator

router = APIRouter(tags=["messages"], prefix="/messages")


@router.get("/welcome")
def welcome_message(
    language: str = Depends(get_language),
    _: Callable[[str], str] = Depends(get_translator),
):
    return {
        "language": language,
        "message": _("Welcome to the expense management API"),
    }


@router.get("/status")
def status_message(_: Callable[[str], str] = Depends(get_translator)):
    return {"message": _("The API is running successfully")}


@router.get("/help")
def help_message(_: Callable[[str], str] = Depends(get_translator)):
    return {"message": _("Send lang=en or lang=fa to choose response language")}
