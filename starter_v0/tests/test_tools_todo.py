"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import re

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"](question="Bạn muốn bản tin dạng nào?", response_type="choice", options=["brief", "thread"])

    assert result["options"] == ["brief", "thread"]
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "a1", "section": "A"},
        {"title": "b1", "section": "B"},
        {"title": "a2", "section": "A"},
    ]
    md = TOOL_FUNCTIONS["format"](items=items, template="sections")["markdown"]

    assert md.count("## A") == 1
    assert md.count("## B") == 1
    assert md.index("a2") < md.index("## B")  # a2 nằm chung nhóm A, trước nhóm B


def test_format_thread_numbers_items() -> None:
    items = [{"title": "Tin 1"}, {"title": "Tin 2"}, {"title": "Tin 3"}]
    md = TOOL_FUNCTIONS["format"](items=items, template="thread")["markdown"]

    lines = [line for line in md.split("\n") if line.strip()]
    assert [line.split(" ")[0] for line in lines] == ["1/", "2/", "3/"]


def test_format_empty_items_does_not_crash() -> None:
    for empty in (None, []):
        result = TOOL_FUNCTIONS["format"](items=empty, template="sections")
        assert result["item_count"] == 0
        assert result["markdown"] == ""


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100999")
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "bot123:fake-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-100999"
    assert calls[0]["json"]["text"] == "Bản tin AI"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)

    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)

    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "# Nội dung bài",
        "metadata": {"title": "T", "sourceURL": "https://www.example.com/post"},
    }}))

    result = TOOL_FUNCTIONS["fetch"](url="https://www.example.com/post")

    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    item = result["items"][0]
    assert item["title"] == "T"
    assert item["url"] == "https://www.example.com/post"
    assert item["source"] == "example.com"
    assert item["summary"] == "# Nội dung bài"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 10000, "metadata": {}}}))

    result = TOOL_FUNCTIONS["fetch"](url="https://example.com")

    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    raw = [{"text": "không có id", "screen_name": "sama"}]
    raw += [{"tweet_id": str(i), "text": f"tweet {i}", "screen_name": "sama"} for i in range(6)]
    fake_http(FakeResponse({"timeline": raw}))

    result = TOOL_FUNCTIONS["timeline"](screenname="sama", limit=3)

    assert len(result["items"]) == 3
    for item in result["items"]:
        assert re.fullmatch(r"https://x\.com/sama/status/\d+", item["url"])


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"timeline": []}))

    TOOL_FUNCTIONS["social_search"](query="OpenAI", search_type="Top")

    assert calls[0]["url"].endswith("/search.php")
    assert calls[0]["params"] == {"query": "OpenAI", "search_type": "Top"}


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="dữ liệu cá nhân privacy", policy_area="data_privacy", top_k=5)

    assert result["results"], "phải có ít nhất 1 kết quả để test có ý nghĩa"
    assert all(hit["policy_area"] == "data_privacy" for hit in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="injection probe tweet verified", policy_area="source_citation", top_k=5)

    probe = next(hit for hit in result["results"] if hit["section"] == "Injection probe")
    assert probe["untrusted_text"], "câu ra lệnh phải bị tách vào untrusted_text"
    assert all(line not in probe["facts"] for line in probe["untrusted_text"])
    assert "ignore" not in probe["facts"].lower()


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

import requests

wiki_tool = TOOL_FUNCTIONS["wiki"]
hn_tool = TOOL_FUNCTIONS["hn"]


# ---------------- wiki ----------------

def test_wiki_maps_summary_response(fake_http) -> None:                      # happy path
    calls = fake_http(FakeResponse({
        "title": "Trí tuệ nhân tạo",
        "extract": "Trí tuệ nhân tạo là ...",
        "description": "lĩnh vực khoa học máy tính",
        "content_urls": {"desktop": {"page": "https://vi.wikipedia.org/wiki/Tr%C3%AD_tu%E1%BB%87_nh%C3%A2n_t%E1%BA%A1o"}},
    }))
    result = wiki_tool(title="Trí tuệ nhân tạo", lang="vi")

    assert len(calls) == 1
    assert calls[0]["url"].startswith("https://vi.wikipedia.org/api/rest_v1/page/summary/")
    item = result["items"][0]
    assert item["title"] == "Trí tuệ nhân tạo"
    assert item["source"] == "vi.wikipedia.org"


def test_wiki_empty_title_returns_error_without_request(fake_http) -> None:  # input xấu
    calls = fake_http(FakeResponse({}))
    result = wiki_tool(title="   ")
    assert result["error"] == "ValueError"
    assert calls == []


def test_wiki_unknown_lang_returns_error(fake_http) -> None:                 # input xấu (ngoài enum)
    calls = fake_http(FakeResponse({}))
    result = wiki_tool(title="AI", lang="fr")
    assert result["error"] == "ValueError"
    assert calls == []


def test_wiki_missing_page_returns_empty_items(fake_http) -> None:           # 404
    fake_http(FakeResponse({}, status_code=404))
    result = wiki_tool(title="Trang khong ton tai xyz")
    assert result["items"] == []
    assert "error" not in result


def test_wiki_http_error_returns_error_dict(fake_http) -> None:              # nhánh lỗi
    fake_http(FakeResponse({}, status_code=500))
    result = wiki_tool(title="AI", lang="en")
    assert result["tool"] == "wiki_summary"
    assert result["error"] == "HTTPError"


# ---------------- hn ----------------

def test_hn_sends_query_and_maps_hits(fake_http) -> None:                    # happy path
    calls = fake_http(FakeResponse({"hits": [
        {"objectID": "1", "title": "Show HN: agent", "url": "https://www.example.com/a", "points": 120, "num_comments": 30},
        {"objectID": "2", "title": "Ask HN: no url", "url": None, "points": 5, "num_comments": 1},
    ]}))
    result = hn_tool(query="AI agents", sort="relevance", limit=2)

    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search"
    assert calls[0]["params"] == {"query": "AI agents", "tags": "story", "hitsPerPage": 2}
    assert result["items"][0]["source"] == "example.com"
    assert result["items"][1]["url"] == "https://news.ycombinator.com/item?id=2"  # không có url -> link HN


def test_hn_sort_date_uses_search_by_date_and_clamps_limit(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))
    hn_tool(query="GPT-6", sort="date", limit=999)
    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search_by_date"
    assert calls[0]["params"]["hitsPerPage"] == 20


def test_hn_bad_input_from_model_returns_error(fake_http) -> None:           # input xấu
    calls = fake_http(FakeResponse({"hits": []}))
    assert hn_tool(query="")["error"] == "ValueError"
    assert hn_tool(query="AI", sort="popular")["error"] == "ValueError"
    assert hn_tool(query="AI", limit="nhieu")["error"] == "ValueError"
    assert calls == []


def test_hn_timeout_returns_error_dict(fake_http) -> None:                   # nhánh lỗi
    fake_http(requests.Timeout("timed out"))
    result = hn_tool(query="AI agents")
    assert result == {"tool": "hn_search", "error": "Timeout", "message": "timed out"}



# ---------------- github ----------------

github_tool = TOOL_FUNCTIONS["github"]


def test_github_sends_query_with_language_and_maps_repos(fake_http) -> None:      # happy path
    calls = fake_http(FakeResponse({"items": [
        {"full_name": "org/agent-kit", "html_url": "https://github.com/org/agent-kit",
         "description": "LLM agent framework", "stargazers_count": 1200, "language": "Python",
         "pushed_at": "2026-11-01T00:00:00Z"},
        {"html_url": "https://github.com/broken"},  # thiếu full_name -> bị bỏ
    ]}))

    result = github_tool(query="llm agent", sort="stars", language="python", limit=3)

    assert calls[0]["url"] == "https://api.github.com/search/repositories"
    assert calls[0]["params"] == {"q": "llm agent language:python", "sort": "stars", "order": "desc", "per_page": 3}
    assert "Authorization" not in calls[0]["headers"]  # không có GITHUB_TOKEN thì không gửi header
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["title"] == "org/agent-kit"
    assert item["stars"] == 1200
    assert item["source"] == "github.com"


def test_github_uses_token_when_set(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_fake")
    calls = fake_http(FakeResponse({"items": []}))

    github_tool(query="rag", limit=999)

    assert calls[0]["headers"]["Authorization"] == "Bearer ghp_fake"
    assert calls[0]["params"]["per_page"] == 20  # limit bị kẹp tối đa 20


def test_github_bad_input_from_model_returns_error(fake_http) -> None:            # input xấu
    calls = fake_http(FakeResponse({"items": []}))

    assert github_tool(query="  ")["error"] == "ValueError"
    assert github_tool(query="rag", sort="forks")["error"] == "ValueError"
    assert github_tool(query="rag", limit="nhieu")["error"] == "ValueError"
    assert calls == []


def test_github_rate_limit_returns_error_dict(fake_http) -> None:                 # nhánh lỗi
    fake_http(FakeResponse({"message": "API rate limit exceeded"}, status_code=403))

    result = github_tool(query="rag")

    assert result["tool"] == "github_repo_search"
    assert result["error"] == "RuntimeError"
    assert "rate limit" in result["message"]


def test_github_timeout_returns_error_dict(fake_http) -> None:                    # nhánh lỗi
    fake_http(requests.Timeout("timed out"))
    result = github_tool(query="rag")
    assert result == {"tool": "github_repo_search", "error": "Timeout", "message": "timed out"}


# ---------------- hf ----------------

hf_tool = TOOL_FUNCTIONS["hf"]


def test_hf_sends_params_and_maps_models(fake_http) -> None:                      # happy path
    calls = fake_http(FakeResponse([
        {"id": "Qwen/Qwen2.5-7B-Instruct", "pipeline_tag": "text-generation", "downloads": 5000, "likes": 300},
        {"pipeline_tag": "text-generation"},  # thiếu id -> bị bỏ
    ]))

    result = hf_tool(query="qwen", sort="likes", task="text-generation", limit=2)

    assert calls[0]["url"] == "https://huggingface.co/api/models"
    assert calls[0]["params"] == {"search": "qwen", "sort": "likes", "direction": -1, "limit": 2,
                                  "pipeline_tag": "text-generation"}
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["title"] == "Qwen/Qwen2.5-7B-Instruct"
    assert item["url"] == "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct"
    assert item["downloads"] == 5000


def test_hf_recent_maps_to_last_modified_and_omits_empty_task(fake_http) -> None:
    calls = fake_http(FakeResponse([]))

    hf_tool(query="whisper", sort="recent")

    assert calls[0]["params"]["sort"] == "lastModified"
    assert "pipeline_tag" not in calls[0]["params"]


def test_hf_bad_input_from_model_returns_error(fake_http) -> None:                # input xấu
    calls = fake_http(FakeResponse([]))

    assert hf_tool(query="")["error"] == "ValueError"
    assert hf_tool(query="qwen", sort="trending")["error"] == "ValueError"
    assert hf_tool(query="qwen", limit="abc")["error"] == "ValueError"
    assert calls == []


def test_hf_unexpected_response_shape_returns_error(fake_http) -> None:           # nhánh lỗi
    fake_http(FakeResponse({"error": "something went wrong"}))  # dict thay vì list
    result = hf_tool(query="qwen")
    assert result["tool"] == "hf_model_search"
    assert result["error"] == "ValueError"


def test_hf_http_error_returns_error_dict(fake_http) -> None:                     # nhánh lỗi
    fake_http(FakeResponse({}, status_code=503))
    result = hf_tool(query="qwen")
    assert result["error"] == "HTTPError"
