# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.


## 1. Thông tin thành viên

- Họ tên: Đặng Thùy Dung
- MSSV: 2A202604116
- Email: dangthuydung1410@gmail.com
- Vai trò: P4 — Eval + Test (hỗ trợ nhóm trưởng Nga)

## 2. Phần việc phụ trách

- Soạn bản đầu bộ eval nhóm `starter_v0/data/eval_group.json`.
- Soạn case và unit test cho các tool mới `wiki`, `hn`.
- Hỗ trợ nhóm trưởng (Nga) hoàn thiện eval nhóm, regression test và kiểm thử.

## 3. Đóng góp cụ thể

**Eval nhóm.** Đọc `eval_base.json` để nắm schema (`query`/`turns`, `failure_type`, `expect`, `metadata.what_it_tests`), rồi soạn bản đầu của `eval_group.json` gồm các case phủ routing, giá trị tham số, không cần tool, thiếu thông tin và ranh giới gửi/đăng. Có case cho tool mới `wiki` (tham số `title`, `lang`) và `hn` (tham số `sort`, `limit`), thiết kế để không trùng bộ base (ví dụ `search_type=Latest`, `timeframe=month`, ranh giới `wiki`/`hn` với `lookup`). Sau đó cùng nhóm trưởng chỉnh lại thành đúng 5 single-turn + 5 multi-turn: giữ 7 case cũ, 1 case `wiki` và các case multi-turn cho tool mới (`github`, `hf`, `hn`). Kết quả group v4 = 10/10 (xem B3 báo cáo nhóm).

**Unit test.** Soạn test offline (mock bằng `fake_http`) cho `wiki` (happy path, title rỗng, lang ngoài enum, 404, lỗi HTTP) và `hn` (map kết quả, sort/limit, input xấu, timeout), mỗi tool ≥ 3 test, theo quy tắc tool lỗi thì trả error dict, không raise. Kết quả `pytest` toàn bộ: 126 passed, 0 failed, 0 skipped.

**Tìm bug.** Khi đọc code `hn_search`, nhận thấy `int(limit or 5)` làm `limit=0` thành 5 trong khi TOOL.md ghi `limit` kẹp trong [1, 20]; đã báo nhóm để xem xét. Bug `limit=-1` của `timeline`/`social_search` do nhóm trưởng phát hiện, sửa và viết test hồi quy.

**Hỗ trợ môi trường và nhóm.** Gặp và xử lý các lỗi setup: key `.env` không nạp do thiếu `python-dotenv` và do chạy lệnh thủ công không qua script có `load_dotenv()`; file `.env.example` trong thư mục OneDrive hiển thị như bị xóa do trạng thái đồng bộ (đã kiểm tra bằng `dir -Force`). Phối hợp với nhóm trưởng để hai phần eval và test không trùng nhau.

## 4. Bằng chứng

- File/commit/PR:
  - [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json) — commit `HASH_EVAL`
  - [`starter_v0/tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) — commit `HASH_TEST`
  - PR: `LINK_PR`
  - Run eval nhóm: [`v4_B_group_openai_20261110T193007162654.json`](../../starter_v0/runs/v4_B_group_openai_20261110T193007162654.json)
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng Claude để hiểu schema eval và gợi ý case/test mẫu. Tự kiểm tra bằng cách kiểm tra JSON hợp lệ và đếm đủ 5 single + 5 multi, đối chiếu tên tool và tham số với `tools.yaml`/TOOL.md, chạy `pytest` để xem còn skip hay fail, và chỉ ghi vào báo cáo số liệu có trong run JSON hoặc commit.

## 5. Tự đánh giá

- **Làm được:** soạn bản đầu bộ eval nhóm phủ cả tool cũ và tool mới; viết test offline cho tool mới; hỗ trợ nhóm trưởng chỉnh eval cho đủ 5 + 5.
- **Chưa tốt:** mất nhiều thời gian ở bước setup (`.env`, môi trường Python, OneDrive) nên phần chạy suite group và sửa bug hồi quy do nhóm trưởng hoàn thành.
- **Bài học:** case eval cần chặt vừa đủ (so khớp `title` hoa/thường có thể làm case FAIL oan); unit test bắt được lỗi biên như `limit=-1` mà eval dùng câu hỏi tự nhiên gần như không chạm tới.
- Bài học: case eval cần chặt vừa đủ (so khớp `title` hoa/thường có thể làm case FAIL oan); test biên giúp bắt lỗi mà eval trên LLM không bắt được.
- Nếu có thêm thời gian: bổ sung case kiểm tra nội dung câu hỏi xác nhận của `clarify` (R12 hiện chỉ chấm `response_type`), và thêm test cho các tool có sẵn.
...
