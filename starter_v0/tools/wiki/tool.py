from __future__ import annotations

from typing import Any
from urllib.parse import quote

import requests

from tools._shared import TIMEOUT, err

ALLOWED_LANGS = {"vi", "en"}


def wiki_summary(title: str = "", lang: str = "vi") -> dict[str, Any]:
    try:
        title = (title or "").strip()
        if not title:
            raise ValueError("title must be a non-empty string")
        lang = (lang or "vi").strip().lower()
        if lang not in ALLOWED_LANGS:
            raise ValueError(f"lang must be one of {sorted(ALLOWED_LANGS)}, got {lang!r}")

        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}"
        response = requests.get(
            url,
            headers={"User-Agent": "AI20k-Day03-Research-Agent/1.0 (educational lab)"},
            timeout=TIMEOUT,
        )
        if response.status_code == 404:
            return {"tool": "wiki_summary", "title": title, "lang": lang, "items": [], "message": "Page not found"}
        response.raise_for_status()
        data = response.json()
        page_url = (data.get("content_urls") or {}).get("desktop", {}).get("page")
        items = [{
            "title": data.get("title"),
            "url": page_url,
            "source": f"{lang}.wikipedia.org",
            "summary": (data.get("extract") or "")[:1500],
            "description": data.get("description"),
        }]
        return {"tool": "wiki_summary", "title": title, "lang": lang, "items": items}
    except Exception as exc:
        return err("wiki_summary", exc)
