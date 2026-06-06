from gettext import NullTranslations, translation
from pathlib import Path
from typing import Callable

from fastapi import Depends, Header, Query

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / "locales"
DOMAIN = "messages"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {"en", "fa"}


def normalize_language(language: str | None):
    if not language:
        return DEFAULT_LANGUAGE

    language = language.lower().replace("_", "-").strip()
    short_language = language.split("-")[0]

    if short_language in SUPPORTED_LANGUAGES:
        return short_language
    return DEFAULT_LANGUAGE


def get_language_from_accept_language(accept_language: str | None):
    if not accept_language:
        return DEFAULT_LANGUAGE

    first_language = accept_language.split(",")[0]
    return normalize_language(first_language)


def get_language(
    lang: str | None = Query(default=None),
    accept_language: str | None = Header(default=None, alias="Accept-Language"),
):
    if lang:
        return normalize_language(lang)
    return get_language_from_accept_language(accept_language)


def get_translator(language: str = Depends(get_language)) -> Callable[[str], str]:
    try:
        translator = translation(DOMAIN, localedir=LOCALE_DIR, languages=[language])
    except FileNotFoundError:
        translator = NullTranslations()

    return translator.gettext
