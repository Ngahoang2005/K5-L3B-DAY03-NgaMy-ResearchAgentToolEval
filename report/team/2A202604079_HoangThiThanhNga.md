# Báo cáo cá nhân — Hoàng Thị Thanh Nga — 2A202604079

## 1. Thông tin thành viên

- Họ tên: Hoàng Thị Thanh Nga
- MSSV: 2A202604079
- Email: hoangthanhnga2005@gmail.com
- GitHub: Ngahoang2005
- Vai trò: P1 — Nhóm trưởng + System prompt

## 2. Phần việc phụ trách

- Nhóm trưởng: tạo repo nhóm, chia việc cho 5 thành viên, điều phối thứ tự chạy các version để mỗi version chỉ đổi một giả thuyết, merge nhánh của thành viên.
- Baseline v0 và phân tích lỗi (C1).
- `system_prompt.md` và các vòng tối ưu v1, v3, v4 (C2, C3).
- Tổng hợp báo cáo nhóm: B1, B2, B3, B5, mục 3 (Giải pháp), mục 5 (Khó khăn), B6 (Reflection), mục 8.
- Làm thay phần còn thiếu của P4: hoàn thiện eval nhóm 10 case, chạy `--suite group`, tìm bug và viết regression test.

## 3. Đóng góp cụ thể

**Setup.** Cấu hình `.env` (model provider, Tavily, Firecrawl, RapidAPI), kiểm tra từng key bằng smoke test và `pytest`. Run v0 đầu tiên dùng Gemini free tier bị 2/20 case lỗi 429 (hết quota 5 request/phút, 20 request/ngày) nên không hợp lệ. Tôi chuyển sang OpenAI `gpt-4o-mini` và giữ cùng provider/model cho mọi version để số đo so sánh được.

**v0 — baseline (0.70).** Chạy prompt + tools gốc của starter: 14/20 PASS. Phân loại 6 case FAIL trong bảng B2. 5/6 lỗi (R08, R10, R11, R12, R14) đến từ 3 chỉ dẫn xấu cố ý trong prompt: đoán thay vì hỏi, gửi không cần xác nhận, ép một tool. Ví dụ R08/R14: câu hỏi toán và yêu cầu viết code bị gửi thẳng lên Telegram bằng `send`.

**v1 — `system_prompt.md` (0.70 → 0.95).** Giả thuyết: thay 3 chỉ dẫn xấu bằng hành vi đúng sẽ sửa 5 case trên. Vẫn chạy với `tools_baseline.yaml` để v1 chỉ khác v0 ở prompt. Kết quả: `tool_routing_accuracy` 0.75 → 1.00; R08, R10, R11, R13, R14 PASS. Còn R12 (`clarify` dạng `text` thay vì `yes_no`), chuyển cho v2 của Huyền.

**v3 — mô tả `policy_area` (extension 0.70 → 1.00).** Sau v2 bộ base đã 1.00, không còn case FAIL để đặt giả thuyết. Tôi chạy bộ extension có sẵn của đề trên v2 (0.70) và tìm được 2 nhóm lỗi: chọn sai `policy_area` (E01, E08) và gọi tuần tự thay vì song song (E06). Chọn một giả thuyết: mô tả `policy_area` quá ngắn và cho dùng `all` "khi chưa rõ". Viết lại mô tả theo loại câu hỏi (không chép câu trong case). Extension đạt 1.00 ở cả 3 run. Base chạy 2 lần: 0.95 (R12 FAIL) và 1.00. Tôi báo cáo cả hai run và kết luận R12 không ổn định, thay vì chỉ giữ run đẹp.

**v4 — thêm tool mới (base 1.00).** Merge nhánh `cp3-tools` của Phương. Khi gặp conflict `tools.yaml`, tôi so từng tool và thấy 10 tool cũ chỉ khác định dạng, nên giữ nội dung v3 và thêm 4 tool mới (`wiki`, `hn`, `github`, `hf`). Chạy lại base để kiểm tra hồi quy: 1.00, thêm tool không gây route nhầm.

**Eval nhóm (làm thay P4).** `eval_group.json` ban đầu có 8 case (6 single + 2 multi), case G05 còn tên tool giả `<TEN_TOOL_MOI>` làm contract test FAIL. Tôi giữ 7 case, viết 3 case multi-turn mới route tới tool mới (G03 `github`, G06 `hf`, G10 `hn`) để đủ 5 + 5 và cả 4 tool mới đều có eval case. Group v4 = 10/10 (bảng B3).

**Regression test (làm thay P4).** Thử input biên trên các tool có sẵn với HTTP giả lập, tìm được bug: `timeline`/`social_search` cắt danh sách bằng `items[: int(limit or 5)]`, nên `limit=-1` trả 9/10 tweet. Viết test trước (FAIL `assert 9 == 5`), sửa cả 2 tool (`limit` ≤ 0 → mặc định 5), test PASS. `pytest`: 126 passed, 0 failed, 0 skipped (mục B5).

**Tính nhất quán của hash.** Phát hiện cùng nội dung `tools.yaml`/`system_prompt.md` nhưng hash khác nhau giữa máy Windows (CRLF) và máy khác (LF). Kiểm chứng bằng cách đổi CRLF → LF thì hash trùng. Thêm `.gitattributes` giữ LF cho `starter_v0/artifacts/*` và chạy lại base v4 để hash prompt khớp v1–v3 (`ea21801f0290`).

## 4. Bằng chứng

- File:
  - [`starter_v0/artifacts/system_prompt.md`](../../starter_v0/artifacts/system_prompt.md) (v1)
  - [`starter_v0/artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml) dòng `policy_area` (v3)
  - [`starter_v0/artifacts/version_log.csv`](../../starter_v0/artifacts/version_log.csv) dòng v0, v1, v3, v4
  - [`.gitattributes`](../../.gitattributes)
  - [Báo cáo nhóm](group_report.md): B1, B2, mục 3, 5, B6
- Run:
  - v0: [`v0_B_base_openai_20261110T174407365229.json`](../../starter_v0/runs/v0_B_base_openai_20261110T174407365229.json)
  - v1: [`v1_B_base_openai_20261110T175638536349.json`](../../starter_v0/runs/v1_B_base_openai_20261110T175638536349.json)
  - v2 extension (tìm lỗi cho v3): [`v2_B_extension_openai_20261110T180957750053.json`](../../starter_v0/runs/v2_B_extension_openai_20261110T180957750053.json)
  - v3: 2 run base, 3 run extension trong [`starter_v0/runs/`](../../starter_v0/runs/)
  - v4: [`v4_B_base_openai_20261110T185650551833.json`](../../starter_v0/runs/v4_B_base_openai_20261110T185650551833.json), group [`v4_B_group_openai_20261110T193007162654.json`](../../starter_v0/runs/v4_B_group_openai_20261110T193007162654.json)
  - Eval nhóm: [`eval_group.json`](../../starter_v0/data/eval_group.json) (G03, G06, G10 và chỉnh lại thành 5 + 5)
  - Regression: [`tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) mục "Regression"; sửa [`timeline`](../../starter_v0/tools/timeline/tool.py), [`social_search`](../../starter_v0/tools/social_search/tool.py)
- Commit: `bcef58c` (v1), `16cec98` (v2 extension + v3), `021b286` và `00adea4` (khôi phục run v0 OpenAI), `c345966` (merge tools.yaml).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng Claude Code để đọc run JSON, phân loại failure, soạn nháp prompt v1, mô tả `policy_area` v3 và báo cáo. Tự kiểm tra bằng cách: chạy eval thật và chỉ dùng run có `provider_error_cases == 0`, `measured_cases == total_cases`; đối chiếu mọi số liệu trong báo cáo với `summary` trong run JSON; chạy `pytest` (contract test) sau mỗi lần sửa `tools.yaml`; chạy lặp lại khi kết quả nghi ngờ (R12).

## 5. Tự đánh giá

- **Làm tốt:** giữ đúng quy tắc mỗi version một giả thuyết (v1 chỉ đổi prompt, v3 chỉ đổi một dòng mô tả). Khi base đã 1.00, tìm được nguồn lỗi thật (bộ extension) thay vì đổi nhãn version. Báo cáo trung thực cả run xấu (R12 ở v3).
- **Chưa tốt:** lúc đầu chưa kiểm tra quota Gemini nên mất một run v0; một lần revert nhầm commit chứa run hợp lệ. Mỗi version chủ yếu chạy 1 lần nên chưa đo được độ dao động một cách hệ thống.
- **Bài học:** điểm 1.00 trên một bộ eval nhỏ không có nghĩa agent không còn lỗi. Cần thêm bộ eval khác và chạy lặp lại để thấy case không ổn định. Hash là bằng chứng nên phải đảm bảo nó ổn định giữa các máy.
