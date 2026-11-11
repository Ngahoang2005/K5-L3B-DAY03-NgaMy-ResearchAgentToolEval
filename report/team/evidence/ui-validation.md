# Kiểm tra UI NgaMy Research

Ngày: 2026-11-10 (GMT+7). UI: Streamlit 1.67.0, Python 3.14.4.

## Kiểm tra offline

`python -m pytest -q`: **70 passed, 17 skipped, 0 failed** ở lần kiểm tra sau khi thêm UI. 17 skip là các stub TODO có sẵn. Tám test mới trong `tests/test_ui.py` xác minh:

- Model tự đặt confirmed=true vẫn không thực thi gửi trước nút xác nhận; xác nhận chỉ chạy một lần.
- Hủy không thực thi action; thay đổi đích không tái sử dụng xác nhận cũ.
- Sai kiểu arguments không gọi implementation.
- Tool mới đăng ký có thể dùng mà không sửa UI.
- Hội thoại giữ câu hỏi làm rõ và dữ liệu tool cho lượt sau.
- Lỗi provider vẫn giữ tool events đã chạy; secret được che trong transcript.
- Streamlit AppTest nhập chat, hiển thị câu trả lời, lưu file và tạo phiên mới không trộn lịch sử.

## Kiểm tra API thật qua UI

Chạy `python scripts/smoke_ui.py` với OpenAI/gpt-4o-mini và Firecrawl. Transcript: [ui_aa9f0caed1b944ce8e41572181c97ca7.transcript.json](../../../starter_v0/transcripts/ui_aa9f0caed1b944ce8e41572181c97ca7.transcript.json).

| Lượt | Tình huống | Kết quả quan sát |
|---|---|---|
| 1 | Thiếu URL cần đọc | answered, không gọi tool; cần review lời hỏi lại, không coi là pass routing clarify |
| 2 | Bổ sung https://example.com | gọi fetch rồi answered |
| 3 | Yêu cầu trình bày lại nội dung | answered trực tiếp, không gọi tool |

Một lần thử trước đó tại [ui_e3bc4d0e17f44924bc250eb5be40d0ea.transcript.json](../../../starter_v0/transcripts/ui_e3bc4d0e17f44924bc250eb5be40d0ea.transcript.json) có fetch và format nhưng câu hỏi tiếng Việt truyền qua terminal bị lỗi mã hóa; chỉ dùng để chẩn đoán, không dùng làm demo chuẩn. Script smoke_ui.py lưu UTF-8 khắc phục vấn đề nhập liệu của lần thử đó.

Không gửi Telegram thật. Luồng xác nhận/hủy đã kiểm tra bằng fake tool offline, chưa xác minh delivery Telegram. Run UI không thay thế `chat.py` hoặc bộ eval chính thức.

## Server và giới hạn xác minh

Tại CP5, test offline mới nhất: `python -m pytest -q` — **128 passed, 0 failed**. Server chạy tại http://127.0.0.1:8501; `GET /_stcore/health` trả `ok`. Đã mở Quick Tunnel tạm thời tại https://perfectly-sell-sector-enormous.trycloudflare.com. Tunnel chỉ hoạt động trong khi tiến trình server và tunnel chạy; chưa có đăng nhập/phân quyền, nên chỉ chia sẻ trong nhóm tin cậy. Browser automation không khả dụng trong môi trường nên chưa kiểm tra screenshot/responsive trực quan; AppTest đã kiểm tra widget và luồng tương tác. Xem [UI-GUIDE](../../../docs/UI-GUIDE.md) trước khi chia sẻ.
