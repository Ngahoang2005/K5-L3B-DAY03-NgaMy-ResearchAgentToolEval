# Team

## Thông tin nhóm

- Tên nhóm: NgaMy (theo tên repo).
- Lớp: L3B.
- Repo nhóm: `K5-L3B-DAY03-NgaMy-ResearchAgentToolEval`.
- URL repo: https://github.com/Ngahoang2005/K5-L3B-DAY03-NgaMy-ResearchAgentToolEval
- Nhánh nộp: `main`. Commit chốt: nhóm trưởng bổ sung khi chốt bài.
- Provider/model dùng cho mọi run eval: `openai / gpt-4o-mini`.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Hoàng Thị Thanh Nga | 2A202604079 | hoangthanhnga2005@gmail.com | Ngahoang2005 | Nhóm trưởng. P1 — System prompt, baseline v0, v1, v3 (C1, C2, C3) |
| 2 | Dương Thị Huyền | 2A202604077 | huyen.dt4002@gmail.com | duongthuyen | P2 — Tool declaration, v2, UI nền Streamlit; bonus local model (C2, C3) |
| 3 | Bùi Thu Phương | 2A202604080 | buithuphuongg1303@gmail.com | buiphuong33 | P3 — Tool mới + unit test (C4) |
| 4 | Đặng Thùy Dung | 2A202604116 | dangthuydung1410@gmail.com | dtdung14 | P4 — Eval case nhóm `eval_group.json` (C5) |
| 5 | Phạm Minh Tâm | 2A202604097 | minhtama11qc@gmail.com | minhtama11qc-hash | P5 — Tinh chỉnh UI, Phần A báo cáo nhóm (C6, C7) |

## Tổng quan kết quả

| Version | Người | Thay đổi | case_accuracy (base) | Run |
|---|---|---|---:|---|
| v0 | Nga | Baseline: prompt + tools starter | 0.70 | `runs/v0_B_base_openai_20261110T174407365229.json` |
| v1 | Nga | `system_prompt.md` | 0.95 | `runs/v1_B_base_openai_20261110T175638536349.json` |
| v2 | Huyền | `tools.yaml` (giữ prompt v1) | 1.00 | `runs/v2_B_base_openai_20261110T180319042654.json` |
| v3 | Nga | `tools.yaml` (`policy_area`) | 0.95 / 1.00 (2 run); extension 0.70 → 1.00 | xem B1 trong [group_report.md](report/team/group_report.md) |

Chi tiết giả thuyết và metric: [version_log.csv](starter_v0/artifacts/version_log.csv) và mục B1 của [group_report.md](report/team/group_report.md).

## Cá nhân

Mỗi thành viên có báo cáo riêng trong `report/team/MSSV_HoTen.md`. Mục dưới tóm tắt phần việc theo bằng chứng trong repo (commit, run, file).

## Hoàng Thị Thanh Nga — 2A202604079

### Phần việc phụ trách

- Nhóm trưởng: tạo repo, điều phối, chốt bài.
- P1: chạy baseline v0, phân tích lỗi (B2), viết system prompt v1, làm v3; ghi `version_log.csv` và B1.

### Đóng góp cụ thể

- v0: chạy baseline với prompt và tools starter. Run Gemini đầu tiên lỗi 429 quota ở 2 case nên đổi sang OpenAI; run OpenAI hợp lệ, 0.70 (14/20). Commit `c4f86f6`, `00adea4`, `021b286`.
- B2: phân tích 6 case FAIL của v0 và gán loại lỗi.
- v1: bỏ 3 chỉ dẫn xấu của prompt starter (đoán thay vì hỏi, gửi không xác nhận, ép một tool), thêm rule routing, clarify và xác nhận gửi. 0.70 → 0.95. Commit `bcef58c`.
- v3: chạy bộ extension trên v2 (0.70), sửa mô tả `policy_area` trong `tools.yaml`; extension 1.00 ở cả 3 run, base 0.95 / 1.00. Ghi nhận R12 dao động giữa các run. Commit `16cec98`.

### Trạng thái

- Báo cáo cá nhân [2A202604079_HoangThiThanhNga.md](report/team/2A202604079_HoangThiThanhNga.md): mới có thông tin thành viên, cần điền mục 2–5.

## Dương Thị Huyền — 2A202604077

### Phần việc phụ trách

- P2: viết mô tả chức năng, khi nào dùng/không dùng và quy ước tham số trong `starter_v0/artifacts/tools.yaml`; `send` chỉ gọi sau xác nhận rõ với `confirmed=true`.
- v2: giữ nguyên prompt v1 của Nga, chỉ thay tool declaration, chạy base eval, ghi `version_log.csv` và B1.
- Bonus (nếu kịp): Small Local Model Challenge qua Ollama, mục B7.

### Đóng góp cụ thể

- Viết lại description 10 tool có sẵn: handle không có `@`, `query` chỉ chứa từ khóa (tin tức dùng `topic=news`), `timeframe`, `Latest`/`Top`, template của `format`, giới hạn trích paper; yêu cầu gửi/đăng luôn bắt đầu bằng `clarify` dạng `yes_no`. Giữ nguyên tên tool và schema; lưu bản starter tại `tools_baseline.yaml` cho v0/v1.
- **v2:** prompt giữ hash v1 (`ea21801f0290`), chỉ đổi tools (`64a6349a4b00`). 0 provider error, 20/20; case_accuracy 0.95 → 1.00; R12 FAIL → PASS, không case nào bị hỏng. Commit `2627635`.
- Xử lý lệch hash do `core.autocrlf` (CRLF làm `prompt_hash` khác v1 dù nội dung giống hệt): đưa file về LF và chạy lại để hash khớp v1.
- **UI Streamlit nền** cho nhóm (`app.py`, `ui_runtime.py`): chat nhiều lượt, hiện tool call và lỗi tool, khung xác nhận gửi, tự lưu transcript. Commit `8c33caf`.
- Merge 4 tool mới của Phương vào `main`, giải conflict `tools.yaml` (giữ mô tả v2, thêm tool mới); đặt UI mặc định dùng prompt và tools đã đo. Commit `f73fb2c`.

### Trạng thái

- Đã xong: declaration, v2, UI nền, báo cáo cá nhân.
- Chưa làm: bonus B7 (máy chưa cài Ollama).

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202604077_DuongThiHuyen.md), [hướng dẫn bàn giao P2](docs/HUYEN-HANDOFF.md), [kiểm tra P2](report/team/evidence/p2-validation.md).
- [tools.yaml](starter_v0/artifacts/tools.yaml), [tools_baseline.yaml](starter_v0/artifacts/tools_baseline.yaml), [run v2](starter_v0/runs/v2_B_base_openai_20261110T180319042654.json).
- [UI-GUIDE.md](docs/UI-GUIDE.md), [kiểm tra UI](report/team/evidence/ui-validation.md).

## Bùi Thu Phương — 2A202604080

### Phần việc phụ trách

- P3: viết tool mới (CP3), mỗi tool có `TOOL.md`, đăng ký trong `tools/__init__.py` và `tools.yaml`, kèm unit test.

### Đóng góp cụ thể

- Thêm 4 tool mới: `wiki` (tóm tắt Wikipedia), `hn` (Hacker News), `github` (tìm repository), `hf` (tìm model Hugging Face). Commit `367b291` (nhánh `buithuphuong/cp3-tools`, đã merge vào `main`).
- Viết unit test offline cho tool trong `tests/test_tools_todo.py`; toàn suite `pytest` 123 passed, 0 skipped.
- Chạy thử baseline v0 trên OpenAI và OpenRouter (nhánh `buithuphuong/runs`, không dùng làm run chính thức).

### Trạng thái

- Báo cáo cá nhân `report/team/2A202604080_BuiThuPhuong`: thiếu đuôi `.md`, cần điền mục 2–5.

## Đặng Thùy Dung — 2A202604116

### Phần việc phụ trách

- P4: viết 10 eval case nhóm trong `starter_v0/data/eval_group.json` (C5).

### Đóng góp cụ thể

- Viết 10 case G01–G10, mỗi case có `expect` và `metadata.what_it_tests`, gồm case route tới tool mới `wiki` (G05) và `hn` (G09, G10). Commit `845805e`, `58fc5a6`, `c21861e`.

### Trạng thái

- Bộ case hiện có 8 single-turn + 2 multi-turn; đề yêu cầu đúng 5 + 5. `github` và `hf` chưa có case (cần cho bonus ≥ 4 tool mới).
- Chưa có run `--suite group` chính thức và bảng B3.
- Báo cáo cá nhân `report/team/2A202604116_DangThuyDung`: thiếu đuôi `.md`, cần điền mục 2–5.

## Phạm Minh Tâm — 2A202604097

### Phần việc phụ trách

- P5: tinh chỉnh UI chat Streamlit và Phần A báo cáo nhóm.

### Đóng góp cụ thể

- Sửa khoảng cách header, ghim ô nhập chat, đổi nhãn tab, nội dung lịch sử rỗng; thêm test AppTest. Commit `f1fa228`, `2d021ca`, `e5b6153`.
- Hoàn thiện Phần A của báo cáo nhóm. Commit `c59d83f`.

### Trạng thái

- Báo cáo cá nhân: [2A202604097_PhamMinhTam.md](report/team/2A202604097_PhamMinhTam.md).
- Còn thiếu cho C6: link UI public, transcript ≥ 3 lượt (yêu cầu thường → thiếu thông tin rồi bổ sung → yêu cầu gửi/đăng) và bảng B4.
