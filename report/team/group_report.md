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

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

NgaMy Research giúp tìm tin web và bài đăng, đọc URL/paper, tra chính sách nội bộ và tổng hợp kết quả có nguồn. UI hỗ trợ hội thoại nhiều lượt, xem tool calls và xác nhận riêng trước khi thực hiện hành động gửi.

**Cách chạy UI:**

Từ `starter_v0/`: `.\.venv\Scripts\python.exe -m streamlit run app.py`. Đã thêm Streamlit và jsonschema vào `requirements.txt`. Hướng dẫn: [UI-GUIDE.md](../../docs/UI-GUIDE.md).

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
URL cục bộ: http://127.0.0.1:8501. Chưa triển khai link public; P5/nhóm cần bổ sung link dùng thử để hoàn tất CP5.

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline / social_search | lấy bài một tài khoản / tìm bài theo từ khóa | không |
| lookup / fetch | tìm nguồn web / đọc URL | không |
| format | định dạng dữ liệu đã có thành digest | không |
| policy | tra chính sách nội bộ | không |
| papers / paper_text | tìm arXiv / đọc trích đoạn paper | không |
| send | gửi Telegram sau xác nhận; cần cấu hình Telegram | không |

UI đọc danh sách động từ declaration; cập nhật bảng này khi nhóm bổ sung tool mới.

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. Tìm 3 tin mới về AI trong tuần qua, tóm tắt kèm nguồn.
2. Lấy 3 bài đăng mới nhất của tài khoản @sama.
3. Đọc https://example.com và tóm tắt nội dung.
4. Đọc bài này giúp mình. (Sau đó bổ sung URL để thử hội thoại nhiều lượt.)
5. Soạn bản tin từ kết quả vừa tìm; yêu cầu gửi Telegram để kiểm tra xác nhận/hủy.

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
| v2 (P2, chờ chạy) | tools.yaml | Làm rõ phạm vi tool/args, giữ prompt v1 để giảm lỗi routing/args | Chưa có run v1 | Chưa đo | Chưa có; xem docs/HUYEN-HANDOFF.md |
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
| UI bổ sung theo yêu cầu của Huyền | `starter_v0/app.py`, `ui_runtime.py`, [hướng dẫn](../../docs/UI-GUIDE.md), [kiểm tra UI](evidence/ui-validation.md) | Chat nhiều lượt, registry động, trace tool, snapshot/hash và tải transcript; local tại cổng 8501 | Prompt UI riêng, guard xác nhận; chưa có link public, không thay điểm eval |

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

**P2 — Huyền: chưa thực hiện bonus.** Chưa có Ollama và bản v3 của nhóm để chạy so sánh. Chưa có run local hay kết luận cải thiện; các bảng dưới là mẫu chưa có số liệu, không diễn giải ô trống thành 0. Xem [hướng dẫn](../../docs/HUYEN-HANDOFF.md) và [bằng chứng kiểm tra P2](evidence/p2-validation.md): offline 62 passed, 17 skipped, 0 failed; preflight OpenAI/gpt-4o-mini PASS. Các kiểm tra này không thay thế local eval.

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
