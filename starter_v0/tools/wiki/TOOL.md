---
name: wiki
track: core
kind: live_api
provider: Wikipedia REST API
requires_env: []
inputs: [title, lang]
outputs: [items]
side_effect: false
---

# wiki

Lấy đoạn tóm tắt của một bài Wikipedia (vi/en). Không cần API key.

- Dùng khi: cần định nghĩa / bối cảnh nền về khái niệm, người, tổ chức.
- Không dùng khi: cần tin mới (dùng `lookup`), cần đọc một URL (dùng `fetch`).
- Lỗi: title rỗng, lang ngoài [vi, en], lỗi HTTP -> error dict. Trang không có (404) -> `items: []`.
