from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err

API_URL = "https://api.github.com/search/repositories"
ALLOWED_SORTS = {"stars", "updated"}


def github_repo_search(query: str = "", sort: str = "stars", language: str = "", limit: int = 5) -> dict[str, Any]:
    try:
        query = (query or "").strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        if sort not in ALLOWED_SORTS:
            raise ValueError(f"sort must be one of {sorted(ALLOWED_SORTS)}, got {sort!r}")
        limit = max(1, min(int(limit or 5), 20))

        q = query
        language = (language or "").strip()
        if language:
            q += f" language:{language}"

        headers = {"Accept": "application/vnd.github+json", "User-Agent": "AI20k-Day03-Research-Agent/1.0"}
        token = os.getenv("GITHUB_TOKEN")  # optional: raises the rate limit, not required
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(
            API_URL,
            params={"q": q, "sort": sort, "order": "desc", "per_page": limit},
            headers=headers,
            timeout=TIMEOUT,
        )
        if response.status_code == 403:
            raise RuntimeError("GitHub API rate limit exceeded; wait a minute or set GITHUB_TOKEN")
        response.raise_for_status()

        items = [{
            "title": repo.get("full_name"),
            "url": repo.get("html_url"),
            "source": "github.com",
            "summary": (repo.get("description") or "")[:300],
            "stars": repo.get("stargazers_count"),
            "language": repo.get("language"),
            "updated_at": repo.get("pushed_at"),
        } for repo in response.json().get("items", []) if repo.get("full_name")]
        return {"tool": "github_repo_search", "query": query, "sort": sort, "items": items[:limit]}
    except Exception as exc:
        return err("github_repo_search", exc)
