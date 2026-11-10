# Team

## Thông tin nhóm

- Tên nhóm: NgaMy (theo tên repo).
- Lớp: L3B.
- Repo nhóm: `K5-L3B-DAY03-NgaMy-ResearchAgentToolEval`.
- URL repo: https://github.com/Ngahoang2005/K5-L3B-DAY03-NgaMy-ResearchAgentToolEval
- Nhánh nộp, commit chốt: nhóm trưởng bổ sung khi chốt bài.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Hoàng Thị Thanh Nga | 2A202604079 | hoangthanhnga2005@gmail.com | Ngahoang2005 | P1 — Nhóm trưởng + System prompt; baseline v0, v1, v3, v4; C1, C2, C3, tổng hợp báo cáo nhóm |
|   2 | Dương Thị Huyền | 2A202604077 | Chưa bổ sung | Chưa bổ sung | P2 — Tool declaration + Local model; C2, C3 và bonus local theo phân công |
|   3 | Phạm Minh Tâm | 2A202604097 | minhtama11qc@gmail.com | minhtama11qc-hash | P5/UI — tinh chỉnh giao diện chat Streamlit (theo commit; nhóm xác nhận phân công chính thức) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

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
- Commit: `bcef58c` (v1), `16cec98` (v2 extension + v3), `021b286`/`00adea4` (v0 OpenAI).

## Dương Thị Huyền — 2A202604077

### Phần việc phụ trách

- Viết mô tả chức năng, khi nào dùng/không dùng và quy ước tham số trong `starter_v0/artifacts/tools.yaml`; quy định `send` chỉ sau xác nhận rõ của người dùng với `confirmed=true`.
- Phụ trách v2: giữ nguyên prompt v1 của Nga, thay tool declaration, chạy base eval và ghi số liệu trước/sau vào `version_log.csv`, bổ sung bằng chứng B1 của báo cáo nhóm.
- Nếu làm bonus: chạy Small Local Model Challenge qua Ollama và hoàn thiện mục B7.

### Đóng góp cụ thể

- Đã viết lại description của 10 tool có sẵn và mô tả tham số: handle không có `@`, `topic=news`, `timeframe`, `Latest`/`Top`, lựa chọn template, giới hạn trích paper và boundary xác nhận gửi.
- Giữ nguyên tên tool và schema; lưu declaration starter tại `tools_baseline.yaml` để P1 vẫn có thể chạy baseline.
- Đã thiết lập môi trường Python và kiểm tra offline: **62 passed, 17 skipped, 0 failed**. Các skip là stub TODO của phần test nhóm; kết quả này không phải điểm eval model.
- Đã kiểm tra kết nối thật: OpenAI `gpt-4o-mini` trả structured tool call; Firecrawl `fetch`, Tavily `lookup`, RapidAPI `social_search` và `timeline` đều trả dữ liệu. `timeline` lỗi lần đầu và thành công khi thử lại; chưa xác định nguyên nhân ban đầu.
- Đã viết báo cáo cá nhân, hướng dẫn API/bàn giao v1 → v2 và cập nhật trạng thái P2 trong báo cáo nhóm. Codex hỗ trợ soạn và đối chiếu implementation; pytest và smoke test được dùng để kiểm tra kết quả.

### Trạng thái và phần còn cần hoàn thành

- **Đã xong:** declaration, kiểm tra offline, kiểm tra API, **v2** và báo cáo.
- **v2 đã chạy:** giữ prompt v1 của Nga (hash `ea21801f0290`), chỉ đổi tools sang `tools.yaml` (hash `64a6349a4b00`); `openai / gpt-4o-mini`, 0 provider error, 20/20. case_accuracy 0.95 → 1.00; R12 FAIL → PASS, không case nào bị hỏng. Đã ghi version_log và B1.
- **Bonus B7 chưa thực hiện:** cần Ollama và bản v3 đã đo của nhóm; chưa có bằng chứng để tính điểm bonus.
- `RULES.md` và `RUBRIC.md` được README nhắc tới nhưng chưa có trong checkout khi thực hiện; cần bổ sung để đối chiếu đầy đủ.
- Email, tài khoản GitHub của Huyền và commit kỹ thuật: chưa bổ sung. Commit kỹ thuật: `8c33caf` và commit v2.

### Bằng chứng

### Đóng góp bổ sung — UI dùng chung

Theo yêu cầu bổ sung của Huyền, đã xây UI Streamlit để thử trước và bàn giao làm nền UI cho P5: chat nhiều lượt, chọn provider/model/prompt/tools, xem tool calls, tải transcript và xác nhận/hủy hành động. Tool mới được nạp qua registry/YAML. Xem [UI-GUIDE.md](docs/UI-GUIDE.md) và [bằng chứng UI](report/team/evidence/ui-validation.md). UI đang phục vụ cục bộ; link public và demo chính thức CP5 vẫn cần nhóm hoàn thiện. Việc này không thay đổi phân công gốc hay được coi là đã hoàn thành v2.

### Bằng chứng P2

- [Báo cáo cá nhân — 2A202604077_DuongThiHuyen.md](report/team/2A202604077_DuongThiHuyen.md).
- [Tool declaration v2](starter_v0/artifacts/tools.yaml) và [declaration starter](starter_v0/artifacts/tools_baseline.yaml).
- [Kết quả kiểm tra P2](report/team/evidence/p2-validation.md).
- [Hướng dẫn setup và bàn giao P2](docs/HUYEN-HANDOFF.md).
- [Báo cáo nhóm — B1 và B7](report/team/group_report.md).
- [Run v2](starter_v0/runs/v2_B_base_openai_20261110T180319042654.json) và dòng v2 trong [version_log.csv](starter_v0/artifacts/version_log.csv).

## Phạm Minh Tâm — 2A202604097

### Phần việc thể hiện trong repo

- Tinh chỉnh UI chat Streamlit dùng chung: sửa khoảng cách đầu trang, bỏ các nút gợi ý, đổi tên tab, đặt thanh nhập cố định ở đáy màn hình trong tab trò chuyện và cập nhật trạng thái trống của lịch sử.
- Đây là các thay đổi có commit của Tâm trong `starter_v0/app.py`; UI nền tảng ban đầu do Dương Thị Huyền thực hiện. Vai trò P5/UI trong bảng thành viên phản ánh các commit hiện có, cần nhóm xác nhận nếu khác phân công chính thức.

### Đóng góp cụ thể và bằng chứng

- [Báo cáo cá nhân — 2A202604097_PhamMinhTam.md](report/team/2A202604097_PhamMinhTam.md).
- Mã và kiểm thử: [app.py](starter_v0/app.py), [test_ui.py](starter_v0/tests/test_ui.py); hướng dẫn: [UI-GUIDE.md](docs/UI-GUIDE.md).
- Commit UI: `f1fa228` (sửa khoảng cách đầu trang), `2d021ca` (tinh chỉnh chat và lịch sử). Commit báo cáo nhóm: `c59d83f`.
- Kiểm tra gần nhất: `python -m pytest -q starter_v0/tests` — **123 passed**.
- Email và username GitHub đã ghi nhận: `minhtama11qc@gmail.com` và `minhtama11qc-hash`.
