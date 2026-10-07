"""VASTU ONE - i18n Routes"""
from __future__ import annotations

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/i18n", tags=["i18n"])

TRANSLATIONS_DIR = Path(__file__).parent.parent / "data" / "translations"
SUPPORTED_LANGS = ["en", "hi", "hinglish"]
DEFAULT_LANG = "en"


def _load_translations(lang: str) -> dict:
    """Load translation JSON for given language."""
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    path = TRANSLATIONS_DIR / f"{lang}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Translation file not found: {lang}")
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/languages")
async def list_languages():
    """List all supported languages."""
    langs = []
    for code in SUPPORTED_LANGS:
        try:
            data = _load_translations(code)
            meta = data.get("_meta", {})
            langs.append({
                "code": code,
                "name": meta.get("name", code),
                "flag": meta.get("flag", ""),
                "dir": meta.get("dir", "ltr"),
            })
        except Exception:
            continue
    return {"languages": langs, "default": DEFAULT_LANG}


@router.get("/translations/{lang}")
async def get_translations(lang: str):
    """Get all translations for a language."""
    return _load_translations(lang)


@router.get("/translations/{lang}/{section}")
async def get_translation_section(lang: str, section: str):
    """Get a specific section of translations."""
    data = _load_translations(lang)
    if section not in data:
        raise HTTPException(status_code=404, detail=f"Section not found: {section}")
    return {section: data[section]}
