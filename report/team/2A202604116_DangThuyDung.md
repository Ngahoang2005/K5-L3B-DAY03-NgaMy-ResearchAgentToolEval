# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.


## 1. Thông tin thành viên

- Họ tên: Đặng Thùy Dung
- MSSV: 2A202604116
- Email: dangthuydung1410@gmail.com
- Vai trò: P4 — Eval + Test 

## 2. Phần việc phụ trách

- Soạn bản đầu bộ eval nhóm `starter_v0/data/eval_group.json` (5 single-turn + 5 multi-turn, tích hợp case dùng tool mới `wiki`, `hn`).
- Phối hợp cùng nhóm trưởng  đóng góp ý tưởng rà soát lỗi biên và định hướng kiểm thử, đồng thời nhờ nhóm trưởng chạy hộ suite group và xác thực kết quả trên môi trường hoàn chỉnh.

## 3. Đóng góp cụ thể

**Eval nhóm.** Đọc `eval_base.json` để nắm schema (`query`/`turns`, `failure_type`, `expect`, `metadata.what_it_tests`), rồi soạn bản đầu của `eval_group.json` gồm các case phủ routing, giá trị tham số, không cần tool, thiếu thông tin và ranh giới gửi/đăng. Có case cho tool mới `wiki` (tham số `title`, `lang`) và `hn` (tham số `sort`, `limit`), thiết kế để không trùng bộ base (ví dụ `search_type=Latest`, `timeframe=month`, ranh giới `wiki`/`hn` với `lookup`). Sau đó cùng nhóm trưởng chỉnh lại thành đúng 5 single-turn + 5 multi-turn: giữ 7 case cũ, 1 case `wiki` và các case multi-turn cho tool mới (`github`, `hf`, `hn`). Kết quả group v4 = 10/10 (xem B3 báo cáo nhóm).

**Unit test.** Soạn test offline (mock bằng `fake_http`) cho `wiki` (happy path, title rỗng, lang ngoài enum, 404, lỗi HTTP) và `hn` (map kết quả, sort/limit, input xấu, timeout), mỗi tool ≥ 3 test, theo quy tắc tool lỗi thì trả error dict, không raise. Kết quả `pytest` toàn bộ: 126 passed, 0 failed, 0 skipped.

**Tìm bug và thảo luận nhóm.** Trong quá trình cùng nhóm trưởng xem xét logic các tool mới (`wiki`, `hn`) và tool cũ, đã cùng thảo luận về các trường hợp input biên (ví dụ tham số `limit=0` hay `limit=-1`). Việc chạy thực thi kiểm tra, bắt bug bằng HTTP mock và sửa code regression test được phối hợp thực hiện cùng nhóm trưởng (Nga) trên môi trường cấu hình API sẵn sàng.

**Hỗ trợ môi trường và nhóm.** Gặp và xử lý các lỗi setup: key `.env` không nạp do thiếu `python-dotenv` và do chạy lệnh thủ công không qua script có `load_dotenv()`; file `.env.example` trong thư mục OneDrive hiển thị như bị xóa do trạng thái đồng bộ (đã kiểm tra bằng `dir -Force`). Phối hợp với nhóm trưởng để hai phần eval và test không trùng nhau.

## 4. Bằng chứng

- File/commit/PR:
  - [`starter_v0/data/eval_group.json`](../../starter_v0/data/eval_group.json)
  -  Commit có thể đối chiếu trong lịch sử Git
  -   `c21861e` Update eval cases
  -   

 
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng Claude để hiểu schema eval và gợi ý case/test mẫu. Tự kiểm tra bằng cách kiểm tra JSON hợp lệ và đếm đủ 5 single + 5 multi, đối chiếu tên tool và tham số với `tools.yaml`/TOOL.md.

## 5. Tự đánh giá

- **Làm được:** Hoàn thành tốt việc soạn thảo bộ 10 eval cases chất lượng cho nhóm, đảm bảo phủ đa dạng các loại lỗi và tool mới.
- **Chưa tốt / Khó khăn:** Máy cá nhân gặp nhiều trở ngại ở khâu cài đặt môi trường, cấu hình API và xung đột đường dẫn, không tự chạy được các script đánh giá nặng. Phải nhờ nhóm trưởng hỗ trợ phần chạy test thực tế.
- **Bài học:** Sức mạnh của làm việc nhóm — khi một thành viên vướng mắc về kỹ thuật môi trường, sự hỗ trợ kịp thời của nhóm trưởng giúp toàn đội tiến độ đúng hạn mà vẫn đảm bảo phân chia rõ ràng phần việc nội dung (eval) và kỹ thuật (chạy pipeline).
- Bài học: case eval cần chặt vừa đủ (so khớp `title` hoa/thường có thể làm case FAIL oan); test biên giúp bắt lỗi mà eval trên LLM không bắt được.
- Nếu có thêm thời gian: bổ sung case kiểm tra nội dung câu hỏi xác nhận của `clarify` (R12 hiện chỉ chấm `response_type`), và thêm test cho các tool có sẵn.
...
