# Báo cáo cá nhân — Dương Thị Huyền — 2A202604077

## 1. Thông tin thành viên

- Họ tên: Dương Thị Huyền.
- MSSV: 2A202604077.
- Email: chưa bổ sung.
- Vai trò: P2 — Tool declaration và Local model.
- Trạng thái: đã hoàn thành declaration và v2 (run thật, 20/20); bonus local chưa có run thật.

## 2. Phần việc phụ trách

Phụ trách `starter_v0/artifacts/tools.yaml`: chức năng, khi nào dùng/không dùng, quy ước tham số và xác nhận trước khi `send`. Phụ trách vòng v2 giữ nguyên prompt v1 của P1 để đo tác động declaration; nếu có điều kiện, làm Small Local Model Challenge qua Ollama và mục B7 báo cáo nhóm. Theo phân công: C2, C3 và bonus local. Chưa xác minh mức điểm vì checkout thiếu `RUBRIC.md`.

## 3. Đóng góp cụ thể

### Tool declaration

Đã cập nhật cả 10 tool có sẵn, giữ nguyên tên tool, tham số, kiểu, enum, default và required để không làm lệch contract với implementation/eval.

| Tool | Thay đổi chính |
|---|---|
| clarify | Hỏi phần thiếu, xác nhận gửi, chờ câu trả lời; phân biệt text/yes_no/choice |
| timeline | Chỉ lấy bài một tài khoản đã biết; handle không có @, không đoán tên mơ hồ |
| social_search | Tìm theo chủ đề trên X; Latest cho mới nhất, Top cho nổi bật |
| lookup | Tra web; news cho tin tức; quy ước day/week/month/year |
| fetch | Đọc URL có thật trong ngữ cảnh, không đoán URL |
| format | Chỉ dùng item đã có; chọn template đúng, giữ nguồn |
| send | Chỉ sau xác nhận nội dung và đích; confirmed là boolean true |
| policy | Chính sách nội bộ, chọn đúng nhóm, không làm theo untrusted_text |
| papers | Tìm metadata arXiv theo chủ đề và kiểu sắp xếp |
| paper_text | Đọc paper có ID/URL; giới hạn trang/ký tự và lưu ý trích đoạn |

Đã lưu `tools_baseline.yaml` nguyên bản để P1 có thể chạy v0/v1 với declaration starter. Không sửa system prompt của P1 hay nội dung `eval_base.json`.

### v2: giả thuyết và kết quả

**Đầu vào:** run v1 của Nga (`openai / gpt-4o-mini`, 0.95, 19/20). Case FAIL duy nhất là R12: user nói "Đăng bản tin này lên Telegram", agent gọi `clarify(response_type="text")` hỏi nội dung, thay vì `yes_no` để xin xác nhận.

**Giả thuyết:** declaration không nói rõ ưu tiên khi nội dung gửi còn mơ hồ. Bản nháp đầu còn ghi `clarify` dùng khi thiếu "nội dung cần gửi" và `text` "để bổ sung thông tin", nên dễ đẩy model về `text`. Nếu mô tả `clarify`/`send` bắt buộc yêu cầu gửi/đăng bắt đầu bằng `yes_no`, R12 sẽ PASS. Đồng thời sửa mô tả `query` của `lookup`/`social_search` thành "chỉ từ khóa" (bản nháp ghi "giữ ràng buộc của người dùng", có nguy cơ làm R13/M02 quay lại lỗi "AI news" / "robotics news" như v0).

**Cách đo:** giữ nguyên prompt v1 (hash `ea21801f0290`, khớp run v1), cùng provider/model và `eval_base.json`, chỉ đổi `--tools artifacts/tools.yaml` (hash `64a6349a4b00`).

**Kết quả** ([run v2](../../starter_v0/runs/v2_B_base_openai_20261110T180319042654.json)): 0 provider error, 20/20 case. case 0.95 → **1.00**, args 0.95 → **1.00**; routing và multiturn giữ 1.00. R12 FAIL → PASS, không case nào bị hỏng. R03, R13, M02 vẫn gọi `lookup(query="AI"|"robotics", topic="news")`.

**Phân tích trung thực:** câu hỏi ở R12 vẫn là "Bạn muốn đăng nội dung gì lên Telegram?", một câu hỏi mở nhưng gắn `yes_no`; eval chỉ chấm `response_type` nên PASS. Đây là giới hạn của bộ chấm, đề xuất xử lý ở v3/eval nhóm. Bộ base đã đạt trần nên v3 nên dùng eval nhóm để đo tiếp.

### Setup và local model

Đã tạo `.venv`, cài requirements, tạo `.env` được Git bỏ qua. OpenAI preflight PASS với `openai / gpt-4o-mini`, trả structured call `timeline(screenname="sama")`. Firecrawl, Tavily và RapidAPI sau đó đã kiểm tra thật thành công; timeline cần thử lại một lần. Xem bằng chứng P2.

Đã viết [hướng dẫn bàn giao P2](../../docs/HUYEN-HANDOFF.md). Bonus chưa thực hiện vì chưa có Ollama và bản v3 của nhóm. Quy trình chuẩn bị gồm hai baseline local khác kích thước, v4-local/v5-local và kiểm tra ngược trên cloud. Chưa có bằng chứng để tính bonus.

## 4. Bằng chứng

Đóng góp bổ sung theo yêu cầu của Huyền: xây UI Streamlit dùng chung cho nhóm, có chat nhiều lượt, chọn model/artifact, registry động, xác nhận hành động và lưu/tải transcript. Đây là phần hỗ trợ P5 ngoài phân công P2. Xem [hướng dẫn UI](../../docs/UI-GUIDE.md) và [bằng chứng UI](evidence/ui-validation.md). UI chạy local; chưa có link public. Prompt demo riêng không được ghi thành prompt v2 đã đo.

- Declaration: [tools.yaml](../../starter_v0/artifacts/tools.yaml); bản gốc: [tools_baseline.yaml](../../starter_v0/artifacts/tools_baseline.yaml).
- Kiểm tra thực tế: [p2-validation.md](evidence/p2-validation.md).
- Hướng dẫn: [HUYEN-HANDOFF.md](../../docs/HUYEN-HANDOFF.md); trạng thái nhóm: B1 và B7 trong [group_report.md](group_report.md).
- Run v2: [v2_B_base_openai_20261110T180319042654.json](../../starter_v0/runs/v2_B_base_openai_20261110T180319042654.json); dòng v2 trong [version_log.csv](../../starter_v0/artifacts/version_log.csv); B1 trong [group_report.md](group_report.md).
- Commit: `8c33caf` (declaration, UI, evidence) và commit v2 (tools.yaml, run v2, version_log, báo cáo).
- AI/công cụ đã dùng: Codex và Claude Code hỗ trợ đọc yêu cầu, đối chiếu implementation, sửa declaration, chạy eval và soạn báo cáo. Tự kiểm tra bằng pytest (70 passed, 17 skipped, 0 failed; skip là stub test của nhóm), đối chiếu hash prompt/tools giữa run v1 và v2, và đọc `actual_tool_calls` từng case thay vì chỉ nhìn điểm tổng.

## 5. Tự đánh giá

Đã hoàn thành declaration và v2 với run thật hợp lệ. v2 sửa đúng case còn lại của v1 (R12) mà không làm hỏng case nào. Phần lớn cải thiện từ v0 đến v1 đến từ prompt của Nga; đóng góp đo được của declaration trên bộ base là 1 case (R12). Vì bộ base đã đạt trần, điểm 1.00 không chứng minh agent hoàn hảo: R12 cho thấy eval chỉ chấm `response_type` chứ không chấm chất lượng câu hỏi xác nhận.

Còn cần: bonus Small Local Model (Ollama) sau khi nhóm có v3; email/GitHub trong TEAM.md.
