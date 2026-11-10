# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Đặng Thùy Dung
- MSSV: 2A202604116
- Email: dangthuydung1410@gmail.com

## 2. Phần việc phụ trách

Vai trò **P4 - Eval + Test** của nhóm Nga My. Phụ trách:

- Viết 10 case eval của nhóm trong `starter_v0/data/eval_group.json` (5 single-turn + 5 multi-turn, có case dùng tool mới) và chạy `--suite group` (mục B3 báo cáo nhóm).
- Điền các stub `pytest.skip` trong `starter_v0/tests/test_tools_todo.py` để đạt 0 skipped.
- Tìm bug trong các tool có sẵn và viết regression test (mục B5).
- Bonus: cùng P3 (Phương) làm thêm tool mới để nhóm đạt ≥ 4 tool.

## 3. Đóng góp cụ thể

**Eval (`data/eval_group.json`)**
- Viết [10] case theo đúng schema của `eval_base.json` (`query` / `turns`, `failure_type`, `expect`, `metadata.what_it_tests`).
- Phủ các loại lỗi: `wrong_tool`, `wrong_arg_value`, `unnecessary_tool`, `missing_info`, `wrong_boundary`. Thiết kế để không trùng với case trong bộ base (ví dụ test `search_type=Latest`, `timeframe=month`, ranh giới `wiki`/`hn` với `lookup`).
- Có [số] case dùng tool mới của nhóm (`wiki`, `hn`, ...), kiểm tra agent chọn đúng tool và đúng tham số (`lang`, `sort`, `limit`).
- Kết quả chạy `--suite group`: [x/10 PASS], run file: `starter_v0/runs/[tên file run]`. Các case FAIL: [liệt kê, nguyên nhân: do agent hay do case viết quá chặt].

**Unit test (`tests/`)**
- Điền [số] stub `pytest.skip` thành test thật; kết quả `pytest`: [số] passed, 0 skipped, 0 failed.
- Viết test cho tool mới ở các tình huống biên: input rỗng, tham số sai giá trị, sai kiểu, và đảm bảo tool trả error dict thay vì raise.

**Tìm bug và regression test (B5)**

| Bug | Input | Kết quả thực tế | Kết quả mong đợi | Test bắt được |
|---|---|---|---|---|
| [tên tool / mô tả] | [input] | [thực tế] | [mong đợi] | `[tên test]` |

(Ví dụ đã nghi ngờ: `hn_search(limit=0)` bị đổi thành 5 vì `int(limit or 5)`, trong khi TOOL.md ghi `limit` kẹp trong [1, 20]. Chỉ giữ dòng này nếu đã xác nhận bằng cách chạy và đã thống nhất cách xử lý với Phương.)

**Tool bonus**
- Tool đã viết: [tên tool], gồm `tool.py`, `TOOL.md`, đăng ký trong `tools/__init__.py` và `tools.yaml`, [số] unit test.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/data/eval_group.json` — commit `[hash]`
  - `starter_v0/tests/test_tools_todo.py` — commit `[hash]`
  - Regression test: `[đường dẫn file test]` — commit `[hash]`
  - PR: [link PR vào main]
  - Run eval nhóm: `starter_v0/runs/[tên file run]`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude để hiểu schema eval, gợi ý case và test mẫu.
  - Tự kiểm tra: kiểm tra JSON hợp lệ và đủ 10 case; chạy `pytest` xem còn skip hay fail; chạy `--suite group` và đối chiếu từng case FAIL với log trong run JSON; chạy thủ công các input biên để xác nhận bug thật trước khi viết regression test; không dùng kết quả của AI khi chưa chạy thử.


## 5. Tự đánh giá

- Làm được: [liệt kê, ví dụ hoàn thành 10 case, 0 skipped, số bug tìm được].
- Chưa làm được / khó khăn: [ví dụ lỗi nạp `.env` ban đầu do thiếu `python-dotenv` và nạp biến môi trường; thư mục dự án nằm trong OneDrive gây lỗi hiển thị file].
- Bài học: case eval cần chặt vừa đủ (so khớp `title` hoa/thường có thể làm case FAIL oan); test biên giúp bắt lỗi mà eval trên LLM không bắt được.
- Nếu có thêm thời gian: bổ sung case kiểm tra nội dung câu hỏi xác nhận của `clarify` (R12 hiện chỉ chấm `response_type`), và thêm test cho các tool có sẵn.
...
