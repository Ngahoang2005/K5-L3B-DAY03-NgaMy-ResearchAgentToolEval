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

Từ `starter_v0/`, cài dependencies bằng `python -m pip install -r requirements.txt`, sau đó chạy `python -m streamlit run app.py`. UI dùng Streamlit; hướng dẫn đầy đủ: [UI-GUIDE.md](../../docs/UI-GUIDE.md).

**Link dùng thử (deploy):**

**Link demo hiện tại:** https://lottery-showed-note-bus.trycloudflare.com (đã kiểm tra health HTTP 200). Đây là Cloudflare Quick Tunnel tạm thời, không phải deployment cố định; chỉ hoạt động khi máy chủ Streamlit và tiến trình tunnel còn chạy. Nếu link hết hạn, chạy lại `cloudflared tunnel --url http://127.0.0.1:8501` và thay URL tại đây. Tunnel không có đăng nhập; chỉ chia sẻ với người tin cậy vì các yêu cầu dùng quota API của máy chủ.

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại khi thiếu thông tin; xin xác nhận trước hành động gửi/đăng. | không |
| `timeline` / `social_search` | Lấy bài từ tài khoản X đã biết / tìm bài X theo chủ đề. | không |
| `lookup` / `fetch` | Tìm web/tin tức / đọc URL đã biết. | không |
| `format` | Định dạng các kết quả đã có thành bản tin/digest có nguồn. | không |
| `policy` | Tra cứu chính sách nội bộ theo chủ đề. | không |
| `papers` / `paper_text` | Tìm paper arXiv / đọc nội dung paper theo ID hoặc URL. | không |
| `send` | Gửi digest lên Telegram sau khi người dùng xác nhận; cần cấu hình Telegram. | không |
| `wiki` | Lấy tóm tắt Wikipedia tiếng Việt hoặc tiếng Anh để tra khái niệm/bối cảnh. | có |
| `hn` | Tìm story Hacker News theo chủ đề, mức liên quan hoặc thời gian. | có |
| `github` | Tìm repository mã nguồn mở, có thể lọc ngôn ngữ và mức phổ biến/cập nhật. | có |
| `hf` | Tìm model AI trên Hugging Face theo từ khóa, tác vụ hoặc độ phổ biến. | có |

Tổng cộng 14 tool; UI hiển thị danh sách từ declaration của phiên. Bốn tool mới được đăng ký trong `starter_v0/tools/` và khai báo trong `starter_v0/artifacts/tools.yaml`.

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. **Yêu cầu thông thường:** “Tìm 3 tin mới về AI trong tuần qua, tóm tắt kèm nguồn.”
2. **Tìm bài đăng:** “Lấy 3 bài đăng mới nhất của tài khoản @sama.”
3. **Thiếu thông tin rồi bổ sung:** “Đọc bài này giúp mình.” Khi agent hỏi URL, gửi tiếp `https://example.com`.
4. **Tổng hợp:** “Tìm 3 bài về AI trên Hacker News và định dạng thành bản tin có nguồn.”
5. **Gửi có xác nhận:** “Soạn bản tin từ kết quả vừa tìm rồi gửi lên Telegram.” Kiểm tra bản nháp và đích; chỉ xác nhận nếu muốn gửi thật. Cần cấu hình Telegram.

Ba tình huống đầu cũng phù hợp làm kịch bản chạy `chat.py`; transcript UI không thay cho bằng chứng chạy CLI nếu đề yêu cầu `chat.py`.

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
| v3                | tools.yaml (`policy` → `policy_area`) | Bộ extension trên v2 = 0.70: E01, E08 chọn sai `policy_area` (`all` / bỏ trống) vì mô tả quá ngắn và cho dùng `all` "khi chưa rõ". Viết lại mô tả từng vùng theo loại câu hỏi, chỉ dùng `all` khi thật sự nhiều vùng | base 1.00 · ext 0.70 | base 0.95 / 1.00 (2 run) · ext 1.00 (3 run) | base: [`…182143417083`](../../starter_v0/runs/v3_B_base_openai_20261110T182143417083.json), [`…182429746542`](../../starter_v0/runs/v3_B_base_openai_20261110T182429746542.json); ext: [`…182208227039`](../../starter_v0/runs/v3_B_extension_openai_20261110T182208227039.json), [`…182515936086`](../../starter_v0/runs/v3_B_extension_openai_20261110T182515936086.json), [`…182637521174`](../../starter_v0/runs/v3_B_extension_openai_20261110T182637521174.json) |

**v2 → v3** (`v2+pea21801f0290+t64a6349a4b00` → `v3+pea21801f0290+t544c396ba964`: prompt giữ nguyên v1, chỉ sửa mô tả `policy_area` trong `tools.yaml`).

Bộ base đã đạt 1.00 ở v2 nên không còn case FAIL để đặt giả thuyết. Nhóm chạy bộ extension có sẵn của đề ([`data/eval_research_extension.json`](../../starter_v0/data/eval_research_extension.json), 10 case về `policy`, `papers`, `paper_text` và gọi nhiều tool) trên v2 để tìm lỗi: [`v2_B_extension_openai_20261110T180957750053.json`](../../starter_v0/runs/v2_B_extension_openai_20261110T180957750053.json) = 0.70, FAIL E01 (`policy_area` = `all` thay vì `source_citation`), E08 (thiếu `policy_area`, cần `ai_research`), E06 (chỉ gọi `policy`, thiếu `lookup`).

| Bộ | v2 | v3 |
|---|---:|---:|
| extension | 0.70 | **1.00** (3/3 run) |
| base | 1.00 | 0.95 (run 1), **1.00** (run 2) |

- Giả thuyết được xác nhận: E01, E08 PASS ổn định ở cả 3 run extension.
- E06 cũng PASS dù v3 không nhắm tới (lỗi E06 là gọi tuần tự, thuộc prompt). Chưa đủ bằng chứng để nói v3 sửa được E06; có thể do dao động của model.
- **R12 không ổn định:** cùng hash v3, run base 1 FAIL R12 (`clarify` dạng `text` thay vì `yes_no`), run 2 PASS. R12 cũng đã đổi qua lại giữa các version (v1 FAIL, v2 PASS). Câu "Đăng bản tin **này**" thiếu nội dung nên model phân vân giữa hỏi nội dung (`text`) và xin xác nhận (`yes_no`). v3 không sửa mô tả `clarify`/`send`, nên lần FAIL này nhiều khả năng do dao động của `gpt-4o-mini` (temperature 0 vẫn không hoàn toàn tất định), không phải do thay đổi `policy_area`.
- Hướng tiếp theo (v4, tùy chọn): thêm rule trong prompt "yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` `yes_no`, kể cả khi thiếu nội dung" để R12 ổn định.

**Ghi chú về hash:** run extension v2 có `tools_hash` `2c04d07a23e7` khác `64a6349a4b00` của run base v2, dù nội dung `tools.yaml` giống hệt. Khác biệt chỉ do kiểu xuống dòng (CRLF trên máy Nga, LF trên máy Huyền); đã kiểm tra bằng cách đổi CRLF → LF thì hash về đúng `64a6349a4b00`.

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

Bảng tổng hợp 10 eval cases trong `starter_v0/data/eval_group.json` (5 single-turn + 5 multi-turn) bao gồm cả các case kiểm thử công cụ mới:

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| **G01_user_tweets_other_person** | Tin của một người cụ thể (Satya Nadella) → routing tới `timeline` với handle `satyanadella`, không dùng `social_search`. | `timeline(screenname="satyanadella")` | PASS |
| **G02_topic_search_latest** | Yêu cầu "mới nhất" → `search_type=Latest` (đối lập với case Top trong bộ base). | `social_search(query="Claude", search_type="Latest")` | PASS |
| **G04_no_tool_greeting** | Trò chuyện xã giao thông thường → trả lời trực tiếp, không gọi bất kỳ tool nào. | `no_tool: true` (`answer_without_tool`) | PASS |
| **G05_wiki_definition_en** | Cần định nghĩa/bối cảnh nền từ Wikipedia → gọi tool mới `wiki` với `title="Alan Turing"`, `lang="en"`, không dùng `lookup` hay `fetch`. | `wiki(title="Alan Turing", lang="en")` | PASS |
| **G09_hn_dev_community** | Hỏi cộng đồng lập trình/tech đang thảo luận gì → gọi tool mới `hn`, không dùng `social_search` hay `lookup`. | `hn(query="Rust")` | PASS |
| **G07_send_confirm_then_fill** | Multi-turn: Dù user đã cung cấp nội dung, hành động gửi vẫn phải xin xác nhận `yes_no` trước, không tự ý gửi. | `clarify(response_type="yes_no")` | PASS |
| **G08_correction_topic_search** | Multi-turn (3 turns): Sửa topic Bitcoin → Ethereum, thêm yêu cầu phổ biến nhất → `query="Ethereum"`, `search_type="Top"`. | `social_search(query="Ethereum", search_type="Top")` | PASS |
| **G03_github_lang_then_sort** | Multi-turn (3 turns): Tìm thư viện mã nguồn mở → tool mới `github`; cộng dồn ràng buộc `language="python"` và `sort="updated"`. | `github(language="python", sort="updated")` | PASS |
| **G06_hf_clarify_then_fill** | Multi-turn (3 turns): Tìm model AI mơ hồ, bổ sung dần → route tới tool mới `hf` (model đã train) với `sort="likes"`. | `hf(sort="likes")` | PASS |
| **G10_hn_followup_sort_date** | Multi-turn (2 turns): Giữ `query="WebAssembly"` từ lượt 1, lượt 2 thêm yêu cầu bài mới nhất → `sort="date"`. | `hn(query="WebAssembly", sort="date")` | PASS |

*Kết quả chung suite group:* **10/10 PASS** (Run artifact: `starter_v0/runs/v4_B_group_openai_20261110T193007162654.json`).

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

Bằng chứng trích xuất từ file transcript phiên chạy trực tiếp (`starter_v0/transcripts/v3_openai_20261110T180412234223.transcript.json`):

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| **1** | Xin chào, hãy giới thiệu ngắn gọn bạn có thể giúp mình nghiên cứu những gì. | *(Không gọi tool)* `[]` | `v3` (`v3_openai_20261110T180412234223`) | **Success** (Trả lời xã giao/giới thiệu năng lực trực tiếp đúng quy tắc `no_tool`, không gọi tool thừa) |

**Ghi chú chi tiết về phiên chạy:**
- **Transcript ID:** `v3_openai_20261110T180412234223`
- **Phiên bản (Version):** `v3` (OpenAI)
- **Hành vi kiểm chứng:** Đối với yêu cầu xã giao/hỏi thông tin chung, Agent phản hồi trực tiếp (`assistant_text`) mà không thực hiện `tool_calls`, đáp ứng chuẩn xác tiêu chí đánh giá không tốn chi phí gọi tool vô ích.

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
