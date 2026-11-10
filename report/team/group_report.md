# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
>
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Nga My
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
> URL cục bộ: http://127.0.0.1:8501. Chưa triển khai link public; P5/nhóm cần bổ sung link dùng thử để hoàn tất CP5.

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool                 | Làm được gì                                      | Tool mới nhóm thêm? |
| ------------------------ | ------------------------------------------------ | ------------------- |
| clarify                  | hỏi lại người dùng khi thiếu thông tin           | không               |
| timeline / social_search | lấy bài một tài khoản / tìm bài theo từ khóa     | không               |
| lookup / fetch           | tìm nguồn web / đọc URL                          | không               |
| format                   | định dạng dữ liệu đã có thành digest             | không               |
| policy                   | tra chính sách nội bộ                            | không               |
| papers / paper_text      | tìm arXiv / đọc trích đoạn paper                 | không               |
| send                     | gửi Telegram sau xác nhận; cần cấu hình Telegram | không               |

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

| Version           | Changed Artifact | Hypothesis                                                       |  Metric Before | Metric After | Run File                           |
| ----------------- | ---------------- | ---------------------------------------------------------------- | -------------: | -----------: | ---------------------------------- |
| v0                | baseline         | Đo hành vi của prompt + tools gốc starter trước khi sửa          |              — |  0.70 (14/20) | [`v0_B_base_openai_20261110T174407365229.json`](../../starter_v0/runs/v0_B_base_openai_20261110T174407365229.json) |
| v1                | system_prompt.md | 5/6 case FAIL ở v0 (R08, R10, R11, R12, R14) do 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một tool). Thay bằng: thiếu thông tin thì `clarify`, gửi phải xác nhận, ngoài phạm vi thì trả lời text, cho phép nhiều tool | 0.70 | 0.95 (19/20) | [`v1_B_base_openai_20261110T175638536349.json`](../../starter_v0/runs/v1_B_base_openai_20261110T175638536349.json) |
| v2                | tools.yaml       | Case FAIL duy nhất của v1 là R12 (`clarify` dạng `text` thay vì `yes_no`) vì declaration không nói ưu tiên xác nhận khi nội dung gửi còn mơ hồ. Giữ prompt v1, thay tool declaration: yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` `yes_no`; `query` chỉ chứa từ khóa (tin tức dùng `topic=news`); mỗi tool nói khi nào dùng/không dùng | 0.95 | 1.00 (20/20) | [`v2_B_base_openai_20261110T180319042654.json`](../../starter_v0/runs/v2_B_base_openai_20261110T180319042654.json) |
| v3                |                  |                                                                  |                |              |                                    |

Tất cả run dùng provider `openai`, model `gpt-4o-mini`, bộ `data/eval_base.json` (20 case), `provider_error_cases == 0`, `measured_cases == 20`.

**v0 → v1** (`artifact_version` `v0+peb1c8179815b+te69bc53ed884` → `v1+pea21801f0290+te69bc53ed884`: chỉ đổi prompt, tools giữ `tools_baseline.yaml`):

| Metric | v0 | v1 |
|---|---:|---:|
| `case_accuracy` | 0.70 | **0.95** |
| `tool_routing_accuracy` | 0.75 | **1.00** |
| `argument_accuracy` | 0.70 | **0.95** |
| `multiturn_accuracy` | 1.00 | 1.00 |

- Giả thuyết được xác nhận: R08, R10, R11, R14 chuyển từ FAIL sang PASS. Agent không còn đoán handle/URL mà gọi `clarify`, không còn gọi `send` cho câu toán/code.
- R13 cũng chuyển sang PASS dù v1 không sửa quy ước tham số. Với prompt mới, `lookup` được gọi với `query="AI"`, `topic="news"`. Điều này cho thấy lỗi tham số ở v0 một phần do chỉ dẫn "làm một bước bằng phán đoán" chứ không chỉ do tool declaration.
- Còn 1 case FAIL: **R12_confirm_before_send** (`wrong_boundary`). Agent đã không gửi ngay (cải thiện so với v0), nhưng gọi `clarify(question="Bạn muốn đăng nội dung gì lên Telegram?", response_type="text")` thay vì `response_type="yes_no"`. Nguyên nhân: user nói "bản tin này" mà không có nội dung, nên agent hỏi nội dung trước. Prompt v1 nói "hỏi xác nhận bằng `yes_no`" nhưng không nói rõ ưu tiên khi vừa thiếu nội dung vừa cần xác nhận. Ứng viên cho v2/v3: mô tả `send`/`clarify` hoặc rule trong prompt rằng yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` dạng `yes_no`.

**v1 → v2** (P2 — Huyền; `artifact_version` `v1+pea21801f0290+te69bc53ed884` → `v2+pea21801f0290+t64a6349a4b00`: prompt giữ nguyên hash, chỉ đổi tools từ `tools_baseline.yaml` sang `tools.yaml`):

| Metric | v1 | v2 |
|---|---:|---:|
| `case_accuracy` | 0.95 | **1.00** |
| `tool_routing_accuracy` | 1.00 | 1.00 |
| `argument_accuracy` | 0.95 | **1.00** |
| `multiturn_accuracy` | 1.00 | 1.00 |

- Giả thuyết được xác nhận: **R12** chuyển FAIL → PASS. Agent gọi `clarify(response_type="yes_no")` thay vì `text`, và không gọi `send`.
- Không có case nào PASS → FAIL. Các case từng sai args ở v0 vẫn đúng: R03/R13 gọi `lookup(query="AI", topic="news", timeframe="day")`, M02 gọi `lookup(query="robotics", topic="news", timeframe="day")`.
- Hạn chế: ở R12, câu hỏi của agent vẫn là "Bạn muốn đăng nội dung gì lên Telegram?", một câu hỏi mở nhưng gắn `response_type="yes_no"`. Eval chỉ chấm `response_type` nên tính PASS; về hành vi thật, câu hỏi nên nêu nội dung cụ thể để người dùng trả lời có/không. Đây là ứng viên cho v3 (prompt), hoặc một case trong `eval_group.json` kiểm tra nội dung câu hỏi xác nhận.
- Điểm base đã chạm trần 20/20, nên v3 khó đo cải thiện trên bộ base. Nên dùng bộ `eval_group.json` của nhóm để tìm lỗi mới.
- Kỹ thuật: máy Huyền dùng `core.autocrlf=true` nên `system_prompt.md` bị đổi sang CRLF, hash khác v1 dù nội dung giống hệt. Đã đưa `system_prompt.md` và `tools.yaml` về LF (đúng bản trong Git) rồi chạy lại để `prompt_hash` khớp v1. Run đầu với CRLF cũng đạt 20/20 nhưng đã bỏ, không nộp.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run: [`starter_v0/runs/v0_B_base_openai_20261110T174407365229.json`](../../starter_v0/runs/v0_B_base_openai_20261110T174407365229.json) — provider `openai`, model `gpt-4o-mini`, prompt + tools gốc của starter. Kết quả 14/20 PASS (`case_accuracy` 0.70, `tool_routing_accuracy` 0.75, `argument_accuracy` 0.70, `multiturn_accuracy` 1.0), `provider_error_cases` 0. 6 case FAIL:

| Case ID                     | Failure Type                               | Actual Tool Calls                                                        | What Failed                                                                                                                                                     | Fix                                                                                                                                            |
| --------------------------- | ------------------------------------------ | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| R08_out_of_scope            | `out_of_scope`                             | `send(text="Nguyên hàm của x^2 là x^3/3 + C…")`                          | Câu hỏi toán ngoài phạm vi, lẽ ra không gọi tool; agent tự giải rồi **đăng lên Telegram**. Nguyên nhân: prompt ép "luôn chọn một tool" và "muốn gửi thì cứ gửi" | Prompt (v1): bỏ "always pick one tool"; thêm rule câu ngoài phạm vi research thì trả lời bằng text, không gọi tool                             |
| R14_out_of_scope_coding     | `out_of_scope`                             | `send(text="Dưới đây là hàm Python tính Fibonacci…")`                    | Yêu cầu viết code ngoài phạm vi, agent lại gọi `send`. Cùng nguyên nhân với R08                                                                                 | Như R08                                                                                                                                        |
| R10_missing_handle          | `missing_info`                             | `timeline(screenname="sama")`                                            | Không có tài khoản nào được nêu, lẽ ra phải `clarify`; agent tự đoán Sam Altman. Nguyên nhân: prompt dặn "pick a well-known account like Sam Altman"            | Prompt (v1): bỏ chỉ dẫn đoán; thêm rule thiếu handle/URL thì gọi `clarify`                                                                     |
| R11_missing_url             | `missing_info`                             | `fetch(url="https://example.com/article")`                               | Không có URL, lẽ ra phải `clarify`; agent bịa URL. Nguyên nhân: prompt dặn "assume a likely URL"                                                                | Như R10                                                                                                                                        |
| R12_confirm_before_send     | `wrong_boundary`                           | `send(text="Bản tin này đã được đăng lên Telegram.")`                    | Lẽ ra phải `clarify(response_type="yes_no")` xin xác nhận trước khi gửi; agent gửi luôn. Nguyên nhân: prompt dặn "just go ahead and do it"                      | Prompt (v1): bỏ chỉ dẫn gửi ngay; thêm rule chỉ gửi khi user đã xác nhận. Tools: mô tả `send` nói rõ chỉ gọi với `confirmed=true` sau xác nhận |
| R13_parallel_web_and_tweets | `wrong_tool` (quan sát: `wrong_arg_value`) | `lookup(query="AI news", timeframe="day")` + `social_search(query="AI")` | Chọn đúng 2 tool nhưng `lookup` sai args: `query` là `"AI news"` thay vì `"AI"`, thiếu `topic="news"`                                                           | Tools (v2): mô tả `lookup` nói rõ `query` chỉ chứa từ khóa, tin tức thì dùng `topic="news"` thay vì thêm chữ "news" vào query                  |

**Nhận xét:** 5/6 case FAIL (R08, R10, R11, R12, R14) đến trực tiếp từ 3 chỉ dẫn xấu cố ý trong `system_prompt.md` của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một tool). Vì vậy giả thuyết v1 là sửa prompt. Case còn lại (R13) là lỗi quy ước tham số, thuộc tool declaration, để cho v2.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
| ------- | ------------- | ---------------------- | ------ |
|         |               |                        |        |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
| ---- | ------------ | ---------- | ---------------- | ------- |
|      |              |            |                  |         |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item                               | Evidence File                                                                                                       | What Worked                                                                                      | Risk / Guardrail                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Tool mới (`tools/<tên>/`)          |                                                                                                                     |                                                                                                  |                                                                            |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed)                                                                                          |                                                                                                  |                                                                            |
| UI (lệnh chạy + link dùng thử)     |                                                                                                                     |                                                                                                  |                                                                            |
| UI bổ sung theo yêu cầu của Huyền  | `starter_v0/app.py`, `ui_runtime.py`, [hướng dẫn](../../docs/UI-GUIDE.md), [kiểm tra UI](evidence/ui-validation.md) | Chat nhiều lượt, registry động, trace tool, snapshot/hash và tải transcript; local tại cổng 8501 | Prompt UI riêng, guard xác nhận; chưa có link public, không thay điểm eval |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus                                        | Evidence File   | What Worked | Risk / Guardrail |
| -------------------------------------------- | --------------- | ----------- | ---------------- |
| Small Local Model                            | xem B7          |             |                  |
| Hơn 3 tool mới (≥ 4)                         |                 |             |                  |
| `send` gửi thật lên Telegram sau xác nhận    | transcript      |             |                  |
| Test challenge (0 skipped / regression test) | `pytest` output |             |                  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

**P2 — Huyền: chưa thực hiện bonus.** Chưa có Ollama và bản v3 của nhóm để chạy so sánh. Chưa có run local hay kết luận cải thiện; các bảng dưới là mẫu chưa có số liệu, không diễn giải ô trống thành 0. Xem [hướng dẫn](../../docs/HUYEN-HANDOFF.md) và [bằng chứng kiểm tra P2](evidence/p2-validation.md): offline 62 passed, 17 skipped, 0 failed; preflight OpenAI/gpt-4o-mini PASS. Các kiểm tra này không thay thế local eval.

| Version    | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
| ---------- | ---------------- | ------------ | ------------- | ------------ | -------- | --------- | -------- |
| v3         | (cloud)          | v3           |               |              |          |           |          |
| v3-<model> | (ollama)         | v3           |               |              |          |           |          |
| v3-<model> | (ollama)         | v3           |               |              |          |           |          |
| v4-local   |                  |              |               |              |          |           |          |
| v5-local   |                  |              |               |              |          |           |          |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern                               | Count | Example Case | Fix Tried | Helped? |
| --------------------------------------------- | ----- | ------------ | --------- | ------- |
| wrong / hallucinated tool                     |       |              |           |         |
| invalid JSON args (`_invalid_json_arguments`) |       |              |           |         |
| no tool call / answered directly              |       |              |           |         |
| missed `clarify`                              |       |              |           |         |
| repeated / unnecessary calls                  |       |              |           |         |

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
