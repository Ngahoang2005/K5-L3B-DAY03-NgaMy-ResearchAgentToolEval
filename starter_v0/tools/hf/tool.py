from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err

API_URL = "https://huggingface.co/api/models"
SORT_FIELDS = {"downloads": "downloads", "likes": "likes", "recent": "lastModified"}


def hf_model_search(query: str = "", sort: str = "downloads", task: str = "", limit: int = 5) -> dict[str, Any]:
    try:
        query = (query or "").strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        if sort not in SORT_FIELDS:
            raise ValueError(f"sort must be one of {sorted(SORT_FIELDS)}, got {sort!r}")
        limit = max(1, min(int(limit or 5), 20))

        params: dict[str, Any] = {"search": query, "sort": SORT_FIELDS[sort], "direction": -1, "limit": limit}
        task = (task or "").strip()
        if task:
            params["pipeline_tag"] = task

        response = requests.get(API_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("Unexpected Hugging Face response: expected a list of models")

        items = [{
            "title": model.get("id"),
            "url": f"https://huggingface.co/{model['id']}",
            "source": "huggingface.co",
            "task": model.get("pipeline_tag"),
            "downloads": model.get("downloads"),
            "likes": model.get("likes"),
            "updated_at": model.get("lastModified"),
        } for model in data if model.get("id")]
        return {"tool": "hf_model_search", "query": query, "sort": sort, "items": items[:limit]}
    except Exception as exc:
        return err("hf_model_search", exc)
