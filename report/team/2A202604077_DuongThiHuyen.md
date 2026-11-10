# Báo cáo cá nhân — Dương Thị Huyền — 2A202604077

## 1. Thông tin thành viên

- Họ tên: Dương Thị Huyền.
- MSSV: 2A202604077.
- Email: chưa bổ sung.
- Vai trò: P2 — Tool declaration và Local model.
- Trạng thái: đã sửa declaration và kiểm tra offline; v2 và bonus local chưa có run thật.

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

### Giả thuyết và kế hoạch đo v2

Giả thuyết: làm rõ phạm vi tool và quy ước arguments sẽ giảm lỗi routing và args so với v1. Giữ nguyên prompt v1, provider/model và bộ case. Đây là một giả thuyết trên toàn bộ declaration; không quy kết mức cải thiện cho từng mô tả nếu chưa có thử nghiệm tách riêng.

Chưa có run v0/v1 và prompt v1 trong checkout. Prompt hiện tại vẫn là starter với chỉ dẫn cố ý sai. Chưa chạy v2, chưa ghi dòng v2 vào version_log, chưa có kết luận tăng điểm. Sau khi P1 bàn giao, so sánh case_accuracy, tool_routing_accuracy, argument_accuracy và multiturn_accuracy; đọc case thay đổi PASS/FAIL. Chỉ dùng run không có provider error và đo đủ case.

### Setup và local model

Đã tạo `.venv`, cài requirements, tạo `.env` được Git bỏ qua. OpenAI preflight PASS với `openai / gpt-4o-mini`, trả structured call `timeline(screenname="sama")`. Firecrawl, Tavily và RapidAPI sau đó đã kiểm tra thật thành công; timeline cần thử lại một lần. Xem bằng chứng P2.

Đã viết [hướng dẫn bàn giao P2](../../docs/HUYEN-HANDOFF.md). Bonus chưa thực hiện vì chưa có Ollama và bản v3 của nhóm. Quy trình chuẩn bị gồm hai baseline local khác kích thước, v4-local/v5-local và kiểm tra ngược trên cloud. Chưa có bằng chứng để tính bonus.

## 4. Bằng chứng

Đóng góp bổ sung theo yêu cầu của Huyền: xây UI Streamlit dùng chung cho nhóm, có chat nhiều lượt, chọn model/artifact, registry động, xác nhận hành động và lưu/tải transcript. Đây là phần hỗ trợ P5 ngoài phân công P2. Xem [hướng dẫn UI](../../docs/UI-GUIDE.md) và [bằng chứng UI](evidence/ui-validation.md). UI chạy local; chưa có link public. Prompt demo riêng không được ghi thành prompt v2 đã đo.

- Declaration: [tools.yaml](../../starter_v0/artifacts/tools.yaml); bản gốc: [tools_baseline.yaml](../../starter_v0/artifacts/tools_baseline.yaml).
- Kiểm tra thực tế: [p2-validation.md](evidence/p2-validation.md).
- Hướng dẫn: [HUYEN-HANDOFF.md](../../docs/HUYEN-HANDOFF.md); trạng thái nhóm: B1 và B7 trong [group_report.md](group_report.md).
- Commit/PR: chưa tạo; cần Huyền review và tạo commit kỹ thuật để ghi nhận đóng góp trong Git.
- AI/công cụ đã dùng: Codex hỗ trợ đọc yêu cầu, đối chiếu implementation, sửa declaration và soạn báo cáo; Python/pytest kiểm tra contract và test hiện có. Kết quả: 62 passed, 17 skipped, 0 failed. Các skip là stub phần test của nhóm, không phải test P2 bị lỗi. Đây không phải điểm eval model.

## 5. Tự đánh giá

Đã hoàn thành phần declaration có thể làm độc lập. Test chứng minh tương thích contract hiện tại, không chứng minh chất lượng routing của model hoặc dữ liệu API. Prompt starter còn xung đột với quy tắc hỏi lại/xác nhận nên P1 cần sửa trước khi đo v2.

Còn cần: prompt/tools và run v1 của Nga; run v2, so sánh số liệu, version_log và kết luận theo log thật. Sau merge đã có run v0 Gemini của nhóm, chưa có v1. Cần thống nhất provider/model trước khi so sánh với máy Huyền đang dùng OpenAI. Bonus chưa hoàn thành. RULES.md/RUBRIC.md được README nhắc tới nhưng đang thiếu nên chưa thể khẳng định đáp ứng toàn bộ rubric gốc. Vòng tiếp theo phải dựa trên failures thật.
