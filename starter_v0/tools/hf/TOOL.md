---
name: hf
track: core
kind: live_api
provider: Hugging Face Hub API
requires_env: []
inputs: [query, sort, task, limit]
outputs: [items]
side_effect: false
---
# hf

Tìm model AI trên Hugging Face Hub. Không cần API key.

- Dùng khi: cần tìm model đã train sẵn (LLM, embedding, ASR...), so sánh độ phổ biến (downloads/likes).
- Không dùng khi: cần code/thư viện (dùng `github`), cần paper (dùng `papers`), cần tin tức (dùng `lookup`).
- `sort`: `downloads`, `likes` hoặc `recent` (mới cập nhật).
- `task`: pipeline tag tuỳ chọn, ví dụ `text-generation`, `automatic-speech-recognition`.
- `limit` bị kẹp trong [1, 20].
- Lỗi: query rỗng, sort sai, response sai dạng, lỗi HTTP/timeout -> error dict, không raise.
