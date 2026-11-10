---
name: hn
track: core
kind: live_api
provider: Hacker News Algolia API
requires_env: []
inputs: [query, sort, limit]
outputs: [items]
side_effect: false
---

# hn

Tìm story trên Hacker News qua Algolia API. Không cần API key.

- Dùng khi: muốn biết cộng đồng dev/tech bàn gì về một chủ đề.
- Không dùng khi: cần tin chính thống (dùng `lookup`) hoặc bài trên X (dùng `social_search`).
- `sort`: `relevance` hoặc `date`. `limit` bị kẹp trong [1, 20].
- Lỗi: query rỗng, sort sai, HTTP lỗi/timeout -> error dict.
