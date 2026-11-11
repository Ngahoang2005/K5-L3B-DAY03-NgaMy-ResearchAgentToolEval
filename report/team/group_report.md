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
- Provider/model dùng cho v0–v3: `openai` / `gpt-4o-mini`, temperature 0 (v4 và các phiên live chat dùng cùng provider/model). Mọi run trong B1 đều có `provider_error_cases == 0`.

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

**`system_prompt.md` (v1, giữ nguyên đến v4, hash `ea21801f0290`).** Bỏ 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép chọn một tool) và thay bằng 4 quy tắc:

- Ngoài phạm vi research thì trả lời bằng text, không gọi tool.
- Thiếu thông tin thì gọi `clarify`, không bịa tài khoản hay URL.
- Gửi/đăng phải xin xác nhận `yes_no` trước, chỉ gọi `send` với `confirmed: true` sau khi người dùng đồng ý.
- Một yêu cầu có thể cần nhiều tool.

**`tools.yaml`.**

- v2: viết lại mô tả 10 tool có sẵn theo dạng khi nào dùng / khi nào không dùng, nêu rõ quy ước tham số (handle không có `@`, `query` chỉ chứa từ khóa, tin tức dùng `topic=news`) và yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` `yes_no`.
- v3: viết lại mô tả `policy_area` theo loại câu hỏi, chỉ dùng `all` khi câu hỏi thật sự thuộc nhiều vùng.
- v4: khai báo 4 tool mới, giữ nguyên nội dung 10 tool cũ.

**Tool mới (không cần API key, lỗi trả error dict).**

| Tool | Làm gì | Agent nên gọi khi |
| --- | --- | --- |
| `wiki` | Tóm tắt một bài Wikipedia (vi/en) | Cần định nghĩa hoặc bối cảnh nền về khái niệm, người, tổ chức |
| `hn` | Tìm story trên Hacker News | Muốn biết cộng đồng dev/tech đang bàn gì về một chủ đề |
| `github` | Tìm repository, lọc theo ngôn ngữ, xếp theo sao hoặc độ mới | Cần thư viện, framework, code mẫu, repo của một dự án |
| `hf` | Tìm model trên Hugging Face, xếp theo lượt tải, like hoặc độ mới | Cần model đã train sẵn hoặc so độ phổ biến của model |

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version           | Changed Artifact | Hypothesis                                                       |  Metric Before | Metric After | Run File                           |
| ----------------- | ---------------- | ---------------------------------------------------------------- | -------------: | -----------: | ---------------------------------- |
| v0                | baseline         | Đo hành vi của prompt + tools gốc starter trước khi sửa          |              — |  0.70 (14/20) | [`v0_B_base_openai_20261110T174407365229.json`](../../starter_v0/runs/v0_B_base_openai_20261110T174407365229.json) |
| v1                | system_prompt.md | 5/6 case FAIL ở v0 (R08, R10, R11, R12, R14) do 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một tool). Thay bằng: thiếu thông tin thì `clarify`, gửi phải xác nhận, ngoài phạm vi thì trả lời text, cho phép nhiều tool | 0.70 | 0.95 (19/20) | [`v1_B_base_openai_20261110T175638536349.json`](../../starter_v0/runs/v1_B_base_openai_20261110T175638536349.json) |
| v2                | tools.yaml       | Case FAIL duy nhất của v1 là R12 (`clarify` dạng `text` thay vì `yes_no`) vì declaration không nói ưu tiên xác nhận khi nội dung gửi còn mơ hồ. Giữ prompt v1, thay tool declaration: yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` `yes_no`; `query` chỉ chứa từ khóa (tin tức dùng `topic=news`); mỗi tool nói khi nào dùng/không dùng | 0.95 | 1.00 (20/20) | [`v2_B_base_openai_20261110T180319042654.json`](../../starter_v0/runs/v2_B_base_openai_20261110T180319042654.json) |
| v3                | tools.yaml (`policy` → `policy_area`) | Bộ extension trên v2 = 0.70: E01, E08 chọn sai `policy_area` (`all` / bỏ trống) vì mô tả quá ngắn và cho dùng `all` "khi chưa rõ". Viết lại mô tả từng vùng theo loại câu hỏi, chỉ dùng `all` khi thật sự nhiều vùng | base 1.00 · ext 0.70 | base 0.95 / 1.00 (2 run) · ext 1.00 (3 run) | base: [`…182143417083`](../../starter_v0/runs/v3_B_base_openai_20261110T182143417083.json), [`…182429746542`](../../starter_v0/runs/v3_B_base_openai_20261110T182429746542.json); ext: [`…182208227039`](../../starter_v0/runs/v3_B_extension_openai_20261110T182208227039.json), [`…182515936086`](../../starter_v0/runs/v3_B_extension_openai_20261110T182515936086.json), [`…182637521174`](../../starter_v0/runs/v3_B_extension_openai_20261110T182637521174.json) |
| v4                | tools.yaml (thêm `wiki`, `hn`, `github`, `hf`) | Thêm tool mới có mô tả khi nào dùng / không dùng rõ ràng sẽ không làm agent route nhầm ở bộ base. Prompt giữ nguyên v1, 10 tool cũ giữ nội dung v3 (`v4+pea21801f0290+t85fc98b68764`) | base 1.00 (v3 run 2; run 1 = 0.95) | base 1.00 (20/20) · group 1.00 (10/10) | base: [`…185650551833`](../../starter_v0/runs/v4_B_base_openai_20261110T185650551833.json); group: [`…193007162654`](../../starter_v0/runs/v4_B_group_openai_20261110T193007162654.json) |

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

Hai phiên chạy thật bằng `chat.py`, provider `openai`, model `gpt-4o-mini`, `artifact_version` `v4+pea21801f0290+t85fc98b68764`.

**Phiên chính:** [`v4_openai_20261111T123937248212.transcript.json`](../../starter_v0/transcripts/v4_openai_20261111T123937248212.transcript.json)

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
| --- | --- | --- | --- | --- |
| 1 | Tìm 3 tin mới về AI trong tuần qua, tóm tắt kèm nguồn (yêu cầu thường) | `lookup(query="AI", topic="news", timeframe="week", max_results=3)` | v4 | Success: 3 kết quả, trả lời kèm nguồn |
| 2 | Xem giúp mình tài khoản X đó mới đăng gì (thiếu thông tin) | Không gọi tool | v4 | Partial: agent hỏi lại tên tài khoản và không đoán, nhưng hỏi bằng text thay vì `clarify` |
| 3 | Tài khoản của Sam Altman, handle là sama, lấy 3 bài thôi (bổ sung) | `timeline(screenname="sama", limit=3)` | v4 | Success: 3 bài đăng |
| 4 | Gửi tóm tắt mấy bài đăng đó lên Telegram giúp mình (yêu cầu gửi) | `clarify(response_type="yes_no")` | v4 | Success: xin xác nhận, chưa gửi |
| 5 | Có, gửi đi | `send(text=...)`, **thiếu `confirmed=true`** | v4 | Fail: tool trả `needs_confirmation`, không có tin nào được gửi; agent hỏi xác nhận lại |

**Phiên phụ:** [`v4_openai_20261111T123840342988.transcript.json`](../../starter_v0/transcripts/v4_openai_20261111T123840342988.transcript.json). Lượt 1 `lookup` thành công, lượt 3 `fetch` một URL người dùng đưa thành công, lượt 4 `clarify` `yes_no` đúng. Hai điểm sai:

- Lượt 2 ("Đọc bài này giúp mình"): agent không hỏi lại mà tự chọn một bài Axios trong kết quả trước để `fetch`.
- Lượt 5: lại gọi `send` không có `confirmed=true`, tool trả `needs_confirmation`; agent báo "chưa thành công".

**Nhận xét:**

- Guardrail trong code của `send` đã chặn đúng khi thiếu xác nhận, nhưng luồng gửi sau khi người dùng đồng ý **thất bại ở 2/2 phiên**. Nguyên nhân khả dĩ: `confirmed` không nằm trong `required` của `send` ở `tools.yaml`. Eval không bắt được lỗi này vì các case gửi dừng ở bước `clarify`.
- Chưa kiểm chứng được gửi Telegram thật: máy chạy phiên này không cấu hình `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`, nên nhóm không nhận bonus gửi thật.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item                               | Evidence File                                                                                                       | What Worked                                                                                      | Risk / Guardrail                                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/wiki/`, `hn/`, `github/`, `hf/`; commit `367b291`, merge `f73fb2c` | 4 tool không cần API key, đủ `tool.py` + `TOOL.md`, đã đăng ký; eval group có case route tới cả 4 (G05, G09, G03, G06, G10) | Validate input, lỗi trả error dict; `limit` kẹp trong [1, 20] (`hn`, `github`, `hf`); GitHub hết rate limit thì báo lỗi rõ |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py`; `pytest`: 126 passed, 0 skipped, 0 failed | 19 test cho 4 tool (wiki 5, hn 4, github 5, hf 5), mỗi tool có happy path, input xấu, nhánh lỗi | HTTP được mock, `block_network` chặn mạng thật; unit test không chứng minh API thật còn đúng định dạng nên cần gọi thử riêng |
| UI (lệnh chạy + link dùng thử)     |                                                                                                                     |                                                                                                  |                                                                            |
| UI bổ sung theo yêu cầu của Huyền  | `starter_v0/app.py`, `ui_runtime.py`, [hướng dẫn](../../docs/UI-GUIDE.md), [kiểm tra UI](evidence/ui-validation.md) | Chat nhiều lượt, registry động, trace tool, snapshot/hash và tải transcript; local tại cổng 8501 | Prompt UI riêng, guard xác nhận; chưa có link public, không thay điểm eval |

Tool unit tests: 19 test cho 4 tool mới. Ví dụ lỗi unit test bắt được nhưng eval không bắt được: nếu bỏ nhánh xử lý HTTP 403 trong `github`, `test_github_rate_limit_returns_error_dict` fail. Eval vẫn không đổi điểm vì `run_eval.py` chỉ chấm tên tool và tham số, không chấm kết quả tool trả về.

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

| Khó khăn | Cách xử lý | Bằng chứng |
| --- | --- | --- |
| Gemini không dùng được ổn định: `gemini-3.8-flash` trả 503/504 khi quá tải, các model khác trả 403 (project không có free tier) hoặc 404 | Chuyển toàn nhóm sang `openai` / `gpt-4o-mini` để mọi version so sánh được với nhau | Lỗi ghi nhận khi preflight, không có run JSON; mọi run trong `starter_v0/runs/` đều dùng OpenAI |
| Cùng nội dung nhưng `prompt_hash` / `tools_hash` khác nhau giữa các máy do CRLF/LF | Đưa file về LF, chạy lại v2; thêm `.gitattributes` | Ghi chú về hash ở B1; run extension v2 có hash `2c04d07a23e7` |
| R12 không ổn định: cùng hash v3 nhưng lần FAIL, lần PASS | Chạy lặp nhiều lần thay vì tin một run, ghi cả hai kết quả | `v3_B_base_openai_20261110T182143417083.json` (0.95), `v3_B_base_openai_20261110T182429746542.json` (1.00) |
| Conflict `tools.yaml` khi merge 4 tool mới với bản mô tả của v2 | Giữ mô tả v2, thêm tool mới, chạy lại base để kiểm tra hồi quy | Commit `f73fb2c`; run `v4_B_base_openai_20261110T185650551833.json` (1.00) |
| Live chat lộ lỗi mà eval không thấy: `send` thiếu `confirmed=true` sau khi người dùng đồng ý | Chưa sửa; ghi lại thành giả thuyết cho vòng sau (mục B6) | Hai transcript ở B4 |
| Link demo Cloudflare Quick Tunnel là tạm thời, tắt máy hoặc tắt lệnh là mất | Phải bật lại khi cần demo và cập nhật URL mới ở A1 | Ghi chú ở A1 |

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Các lỗi do chính sách hành vi: bỏ đoán handle/URL (R10, R11), không gọi tool cho câu ngoài phạm vi (R08, R14), không gửi khi chưa xác nhận (bước đầu của R12). Đây là fix của v1, đưa base từ 0.70 lên 0.95.
- **Fix nào thuộc `tools.yaml`?** Các lỗi về chọn tool và giá trị tham số: `clarify` phải dạng `yes_no` trước khi gửi (R12, v2), chọn đúng `policy_area` (E01, E08, v3). Thêm tool mới cũng thuộc file này (v4).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  - Eval chỉ chấm tên tool và tham số, không chấm kết quả tool trả về hay chất lượng câu trả lời.
  - R12 PASS dù câu hỏi là "Bạn muốn đăng nội dung gì?" gắn `yes_no`, một câu không thể trả lời có/không.
  - Luồng sau xác nhận (`send` thiếu `confirmed=true`) và việc agent tự chọn bài khi người dùng nói "bài này" chỉ lộ ra khi đọc transcript (B4).
  - Sự thay đổi không nhắm tới như E06 PASS ở v3 cần đọc lại, chưa đủ bằng chứng để quy cho fix.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?** Thêm `confirmed` vào `required` của `send` và ghi rõ "sau khi người dùng đồng ý phải truyền `confirmed=true`" sẽ làm luồng gửi hoàn tất mà không làm hỏng case xin xác nhận. Đo bằng case multi-turn mới kết thúc bằng lượt "Có, gửi đi" (kỳ vọng `send(confirmed=true)`), rồi chạy lại base và group. Sau đó thêm case "đọc bài này" ngay sau một danh sách nhiều kết quả, kỳ vọng `clarify`.

## 8. Tài liệu tham khảo

- Tài liệu lab trong repo: [README.md](../../README.md), [RUBRIC.md](../../RUBRIC.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [TOOL-SETUP.md](../../docs/TOOL-SETUP.md), [UI-GUIDE.md](../../docs/UI-GUIDE.md).
- Tavily: https://docs.tavily.com/documentation/api-credits
- Firecrawl: https://docs.firecrawl.dev
- RapidAPI Twitter API45: https://rapidapi.com/alexanderxbx/api/twitter-api45
- Wikipedia REST API: https://en.wikipedia.org/api/rest_v1/
- Hacker News Search API (Algolia): https://hn.algolia.com/api
- GitHub REST API, tìm repository: https://docs.github.com/en/rest/search/search#search-repositories
- Hugging Face Hub API: https://huggingface.co/docs/hub/api
- arXiv API: https://info.arxiv.org/help/api/index.html
- Telegram Bot API: https://core.telegram.org/bots
- Streamlit: https://docs.streamlit.io
