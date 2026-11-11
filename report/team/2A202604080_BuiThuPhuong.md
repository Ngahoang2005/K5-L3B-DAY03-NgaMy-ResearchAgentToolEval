# Báo cáo cá nhân — BuiThuPhuong-2A202604080

## 1. Thông tin thành viên

- Họ tên: Bùi Thu Phương
- MSSV: 2A202604080
- Email: buithuphuongg1303@gmail.com

## 2. Phần việc phụ trách

CP3: viết tool mới và unit test

## 3. Đóng góp cụ thể

- **4 tool mới** (không cần API key), mỗi tool có `tool.py` + `TOOL.md`, đăng ký trong
  `tools/__init__.py` và `artifacts/tools.yaml`:
  - `wiki`: tóm tắt bài Wikipedia (vi/en).
  - `hn`: tìm thảo luận trên Hacker News.
  - `github`: tìm repo mã nguồn mở (hỗ trợ `GITHUB_TOKEN` tuỳ chọn, xử lý hết rate limit).
  - `hf`: tìm model trên Hugging Face Hub.
  - Tất cả validate input và trả error dict khi lỗi, không raise.

- **Unit test:** 19 test cho 4 tool mới (mỗi tool có happy path, input xấu, nhánh lỗi) + viết 14 test
  TODO có sẵn (clarify, format, send, lookup, fetch, timeline, social_search, policy).
  Kết quả: `pytest tests/` → **126 passed, 0 skipped, 0 failed** (toàn suite trên `main`, gồm cả regression test và test UI của nhóm), chạy offline (mock HTTP).

## 4. Bằng chứng

- File/commit/PR:
  - Tool: `starter_v0/tools/wiki/`, `hn/`, `github/`, `hf/`
  - Test: `starter_v0/tests/test_tools_todo.py`
  - Commit `367b291` — CP3: add wiki, hn, github, hf tools with unit tests
  - Commit `ca26407` — Add baseline eval runs (nhánh `buithuphuong/runs`, chưa vào `main`, không dùng làm run chính thức)
  - PR: không có, nhánh được merge trực tiếp vào `main` qua commit `f73fb2c`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude Code để gợi ý cấu trúc tool, viết code và test, debug lỗi setup.
  - Tự kiểm tra: chạy `pytest tests/ -v` (0 failed); chạy `pytest tests/test_tool_contract.py` để chắc
    `tools.yaml` khớp code; gọi thật mỗi tool 1 lần để xác nhận API trả đúng dữ liệu; đọc lại từng
    test để hiểu nó kiểm tra gì (Arrange → Act → Assert, mock bằng `fake_http`).

## 5. Tự đánh giá

- Làm tốt: tool trả error dict đúng contract, test phủ cả nhánh lỗi, không gọi mạng thật trong test.
- Học được: unit test đo code của tool, eval đo lựa chọn tool của model; vì sao phải mock HTTP.
