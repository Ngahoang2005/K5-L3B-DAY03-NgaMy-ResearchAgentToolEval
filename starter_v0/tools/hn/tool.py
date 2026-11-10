from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err

ENDPOINTS = {
    "relevance": "https://hn.algolia.com/api/v1/search",
    "date": "https://hn.algolia.com/api/v1/search_by_date",
}


def hn_search(query: str = "", sort: str = "relevance", limit: int = 5) -> dict[str, Any]:
    try:
        query = (query or "").strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        if sort not in ENDPOINTS:
            raise ValueError(f"sort must be one of {sorted(ENDPOINTS)}, got {sort!r}")
        limit = max(1, min(int(limit or 5), 20))

        response = requests.get(
            ENDPOINTS[sort],
            params={"query": query, "tags": "story", "hitsPerPage": limit},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        items = []
        for hit in response.json().get("hits", []):
            story_id = hit.get("objectID")
            if not story_id:
                continue
            hn_url = f"https://news.ycombinator.com/item?id={story_id}"
            url = hit.get("url") or hn_url
            items.append({
                "title": hit.get("title"),
                "url": url,
                "source": domain(url),
                "hn_url": hn_url,
                "points": hit.get("points"),
                "num_comments": hit.get("num_comments"),
                "created_at": hit.get("created_at"),
            })
        return {"tool": "hn_search", "query": query, "sort": sort, "items": items[:limit]}
    except Exception as exc:
        return err("hn_search", exc)
