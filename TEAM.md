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
| 1 | Hoàng Thị Thanh Nga | 2A202604079 | hoangthanhnga2005@gmail.com | Ngahoang2005 | P1 — Nhóm trưởng + System prompt; baseline v0, v1, v3, v4; C1, C2, C3, tổng hợp báo cáo nhóm |
| 2 | Dương Thị Huyền | 2A202604077 | huyen.dt4002@gmail.com | duongthuyen | P2 — Tool declaration, v2, UI nền Streamlit; bonus local model (C2, C3) |
| 3 | Bùi Thu Phương | 2A202604080 | buithuphuongg1303@gmail.com | buiphuong33 | P3 — Tool mới + unit test (C4) |
| 4 | Đặng Thùy Dung | 2A202604116 | dangthuydung1410@gmail.com | dtdung14 | P4 — Eval case nhóm + test (C5) |
| 5 | Phạm Minh Tâm | 2A202604097 | minhtama11qc@gmail.com | minhtama11qc-hash | P5/UI — tinh chỉnh giao diện chat Streamlit, Phần A báo cáo nhóm (theo commit; nhóm xác nhận phân công chính thức) |

## Tổng quan kết quả

| Version | Người | Thay đổi | Kết quả | Ghi chú |
|---|---|---|---|---|
| v0 | Nga | Baseline: prompt + tools starter | base 0.70 | |
| v1 | Nga | `system_prompt.md` | base 0.95 | |
| v2 | Huyền | `tools.yaml` (giữ prompt v1) | base 1.00 | |
| v3 | Nga | `tools.yaml` (`policy_area`) | base 0.95 / 1.00 (2 run); extension 0.70 → 1.00 | R12 không ổn định giữa các run |
| v4 | Nga | `tools.yaml` thêm 4 tool mới của Phương | base 1.00; group 1.00 | Kiểm tra hồi quy sau khi thêm tool |

Chi tiết giả thuyết, hash và metric: [version_log.csv](starter_v0/artifacts/version_log.csv) và mục B1 của [group_report.md](report/team/group_report.md).

## Cá nhân

Mỗi thành viên có báo cáo riêng trong `report/team/MSSV_HoTen.md`. Mục dưới tóm tắt phần việc theo bằng chứng trong repo (commit, run, file).

## Hoàng Thị Thanh Nga — 2A202604079

### Phần việc phụ trách

- Nhóm trưởng: tạo repo, chia việc, điều phối thứ tự v0 → v4, merge nhánh thành viên.
- P1 — System prompt và vòng lặp tối ưu: baseline v0, v1 (prompt), v3 (`policy_area`), v4 (kiểm tra hồi quy sau khi thêm tool mới).
- Tổng hợp báo cáo nhóm: B1, B2, mục 3, 5, B6, 8.

### Đóng góp cụ thể

- Cấu hình `.env` và provider; xử lý sự cố Gemini hết quota, chuyển toàn nhóm sang OpenAI `gpt-4o-mini`.
- v0: chạy baseline hợp lệ (0.70), phân loại 6 case FAIL (bảng B2).
- v1: viết lại `system_prompt.md`, bỏ 3 chỉ dẫn xấu → base 0.70 → 0.95.
- v3: dùng bộ extension tìm lỗi khi base đã 1.00; sửa mô tả `policy_area` → extension 0.70 → 1.00; chạy lặp base để phát hiện R12 không ổn định.
- v4: merge 4 tool mới của Phương (giữ nội dung v3 cho 10 tool cũ), chạy base kiểm tra hồi quy (1.00).
- Thêm `.gitattributes` để hash prompt/tools giống nhau trên mọi máy.
- Làm thay P4: hoàn thiện `eval_group.json` thành 5 + 5 (viết G03 `github`, G06 `hf`, G10 `hn`), chạy group v4 (10/10), điền B3.
- Tìm bug `limit` âm trong `timeline`/`social_search`, viết 3 regression test, sửa code (`pytest` 126 passed, 0 skipped), điền B5.

### Bằng chứng

- [Báo cáo cá nhân — 2A202604079_HoangThiThanhNga.md](report/team/2A202604079_HoangThiThanhNga.md).
- Run: [v0](starter_v0/runs/v0_B_base_openai_20261110T174407365229.json), [v1](starter_v0/runs/v1_B_base_openai_20261110T175638536349.json), v3 và v4 trong [`starter_v0/runs/`](starter_v0/runs/); dòng v0, v1, v3, v4 trong [version_log.csv](starter_v0/artifacts/version_log.csv).
- Commit: `bcef58c` (v1), `16cec98` (v2 extension + v3), `021b286`/`00adea4` (v0 OpenAI), `e9b2f90` (v4, 10 case eval).

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
- Merge nhánh tool mới của Phương vào `main`, giải conflict `tools.yaml` (giữ mô tả v2, thêm tool mới); đặt UI mặc định dùng prompt và tools đã đo. Commit `f73fb2c`.

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
- Viết unit test offline cho tool trong `tests/test_tools_todo.py`; sau khi merge, toàn suite `pytest` không còn test bị skip.
- Chạy thử baseline v0 trên OpenAI và OpenRouter (nhánh `buithuphuong/runs`, không dùng làm run chính thức).

### Trạng thái

- Báo cáo cá nhân [2A202604080_BuiThuPhuong.md](report/team/2A202604080_BuiThuPhuong.md): đã đổi đúng tên và điền mục 2–5. Dòng Tool mới và Unit test trong bảng B5a đã điền.

## Đặng Thùy Dung — 2A202604116

### Phần việc phụ trách

- P4: viết eval case nhóm trong `starter_v0/data/eval_group.json` (C5), test và tìm bug tool có sẵn.

### Đóng góp cụ thể

- Viết bộ case nhóm ban đầu G01–G10 theo schema của `eval_base.json`, mỗi case có `expect` và `metadata.what_it_tests`, gồm case route tới tool mới `wiki` và `hn`. Commit `845805e`, `58fc5a6`, `c21861e`.
- Phối hợp cùng nhóm trưởng  cấu trúc lại thành chuẩn 5 single-turn + 5 multi-turn, bổ sung case cho `github`, `hf` (commit `e9b2f90`).
- Phối hợp kiểm thử và xác thực kết quả chạy nhóm v4 đạt `10/10 PASS` 


### Trạng thái

- Báo cáo cá nhân [2A202604116_DangThuyDung.md](report/team/2A202604116_DangThuyDung.md):
- Commit `845805e`, `58fc5a6`, `c21861e`.

## Phạm Minh Tâm — 2A202604097

### Phần việc thể hiện trong repo

- Tinh chỉnh UI chat Streamlit dùng chung: sửa khoảng cách đầu trang, bỏ các nút gợi ý, đổi tên tab, đặt thanh nhập cố định ở đáy màn hình trong tab trò chuyện và cập nhật trạng thái trống của lịch sử.
- Đây là các thay đổi có commit của Tâm trong `starter_v0/app.py`; UI nền tảng ban đầu do Dương Thị Huyền thực hiện. Vai trò P5/UI trong bảng thành viên phản ánh các commit hiện có, cần nhóm xác nhận nếu khác phân công chính thức.

### Đóng góp cụ thể và bằng chứng

- [Báo cáo cá nhân — 2A202604097_PhamMinhTam.md](report/team/2A202604097_PhamMinhTam.md).
- Mã và kiểm thử: [app.py](starter_v0/app.py), [test_ui.py](starter_v0/tests/test_ui.py); hướng dẫn: [UI-GUIDE.md](docs/UI-GUIDE.md).
- Commit UI: `f1fa228` (sửa khoảng cách đầu trang), `2d021ca` (tinh chỉnh chat và lịch sử). Commit báo cáo nhóm: `c59d83f`.
- Kiểm tra gần nhất: `python -m pytest -q starter_v0/tests` — **126 passed**.
- Email và username GitHub đã ghi nhận: `minhtama11qc@gmail.com` và `minhtama11qc-hash`.
