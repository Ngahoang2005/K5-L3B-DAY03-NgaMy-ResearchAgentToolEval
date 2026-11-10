# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent là trợ lý nghiên cứu có thể tìm thông tin trên web và X/Twitter, đọc một URL do người dùng cung cấp, tra cứu policy nội bộ hoặc tìm/đọc paper arXiv, sau đó trình bày các kết quả thành digest. Các thao tác cụ thể agent chọn phụ thuộc vào system prompt và tool declarations của version nhóm đang chạy.

**Cách chạy UI:** trong terminal VS Code, chuyển vào `starter_v0/`, cài dependencies bằng `python -m pip install -r requirements.txt`, rồi chạy `streamlit run app.py`. Chọn provider và version ở sidebar. API key đặt trong `starter_v0/.env`; tuyệt đối không đưa file này lên GitHub hoặc vào báo cáo.

**Link dùng thử:** Chưa có URL public. UI đã chạy và được kiểm tra tại `http://127.0.0.1:8501` trên máy phát triển; địa chỉ này chỉ truy cập local. Chỉ bổ sung link Cloudflare Tunnel sau khi nhóm tích hợp prompt/tools CP2, kiểm tra guardrail và xác nhận key dùng cho demo đã an toàn.

**Lưu ý trước demo:** `system_prompt.md` hiện vẫn là prompt starter, trong đó có chỉ dẫn cố ý đoán thông tin còn thiếu và gửi/đăng ngay. Vì vậy chưa được giới thiệu hành vi hỏi lại hoặc xác nhận gửi là đã hoạt động; cần tích hợp và kiểm tra bản CP2 trước. UI đọc `artifacts/system_prompt.md` và `artifacts/tools.yaml` khi bắt đầu phiên mới, đồng thời lưu chat vào `transcripts/*.transcript.json`.

### A2. Tool agent có

> Các tool đã đăng ký trong `tools/__init__.py` và khai báo trong `artifacts/tools.yaml`. Chưa có tool mới do nhóm thêm trong registry hiện tại.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | đặt câu hỏi và tạm dừng để chờ người dùng bổ sung | không |
| timeline | lấy bài đăng gần đây của một tài khoản X | không |
| social_search | tìm bài đăng X theo chủ đề/từ khóa | không |
| lookup | tìm kiếm web, gồm nội dung chung hoặc tin tức | không |
| fetch | đọc nội dung từ một URL cụ thể | không |
| format | định dạng các item đã thu thập thành digest | không |
| send | gửi text tới Telegram khi được gọi với `confirmed=true`; phải kiểm tra xác nhận của prompt trước khi dùng thật | không |
| policy | tìm trong bộ tài liệu policy nội bộ mẫu | không |
| papers | tìm paper/preprint trên arXiv | không |
| paper_text | lấy text từ paper arXiv theo ID hoặc URL | không |

### A3. Câu hỏi mẫu để thử

> Dùng các câu sau để demo routing. Với yêu cầu gửi/đăng, chỉ kiểm tra bản nháp và bước xin xác nhận; không gửi thật trước khi CP2 đã được tích hợp và guardrail được kiểm thử.

1. Tìm tin AI trong ngày và tóm tắt một vài kết quả kèm nguồn.
2. Tìm bài đăng gần đây của tài khoản `@sama`.
3. Đọc và tóm tắt URL `https://openai.com/research/`.
4. Hỏi agent chuẩn bị một bản tin để gửi Telegram; xem agent tạo bản nháp và xử lý xác nhận thế nào. Không xác nhận gửi thật trong demo nếu chưa kiểm thử guardrail CP2.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
