---
name: github
track: core
kind: live_api
provider: GitHub REST API (search/repositories)
requires_env: []
inputs: [query, sort, language, limit]
outputs: [items]
side_effect: false
---
# github

Tìm repository mã nguồn mở trên GitHub. Không bắt buộc API key; nếu có
`GITHUB_TOKEN` trong `.env` thì tool tự dùng để tăng rate limit
(không có token: khoảng 10 lần tìm/phút).

- Dùng khi: cần tìm thư viện, framework, code mẫu, repo chính thức của một dự án/paper.
- Không dùng khi: cần tin tức (dùng `lookup`), cần model đã train (dùng `hf`), cần paper (dùng `papers`).
- `sort`: `stars` (nổi tiếng nhất) hoặc `updated` (mới cập nhật). `language` lọc theo ngôn ngữ, ví dụ `python`.
- `limit` bị kẹp trong [1, 20].
- Lỗi: query rỗng, sort sai, hết rate limit (403), lỗi HTTP/timeout -> error dict, không raise.
