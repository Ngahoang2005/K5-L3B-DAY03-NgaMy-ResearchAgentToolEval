# NgaMy Research — UI dùng chung cho nhóm

## Chạy trên máy

Từ terminal tại thư mục repo:

```powershell
cd starter_v0
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Mở http://127.0.0.1:8501. Giữ terminal chạy trong khi dùng, Ctrl+C để dừng. Nếu cổng đã bận, dùng `--server.port 8502` và mở cổng tương ứng. Các key đã có trong `.env`; không nhập key vào chat. Mỗi tab trình duyệt có phiên riêng.

## Dùng thử

- Sidebar: chọn provider/model và **Version agent** (`v0`–`v4` hoặc **Tùy chỉnh**). Bấm **Áp dụng version & tạo phiên mới** để bắt đầu chat với cấu hình chọn; phiên cũ được lưu trước khi đổi.
- **Trò chuyện:** nhập câu hỏi; trả lời tiếp nếu agent hỏi lại. Ô nhập được cố định ở đáy màn hình và chỉ xuất hiện trong tab này; khi chuyển sang tab khác thì ô nhập được ẩn.
- **Công cụ & cấu hình:** xem toàn bộ tool của phiên, schema, metadata và biến môi trường còn thiếu. Không có giá trị key trong UI.
- **Phiên bản Agent:** xem mục tiêu thay đổi và diff prompt/tool declaration so với version trước. Chọn version trong sidebar để xem diff tương ứng; version chatbot đang chạy chỉ đổi sau khi bấm nút áp dụng.
- **Lịch sử chat:** mỗi lượt ghi version agent và artifact fingerprint tương ứng (cả trong transcript); bảng lịch sử hiển thị version đó cùng yêu cầu/trạng thái. **Tải transcript JSON** trong sidebar để lấy bằng chứng. Server tự lưu sau mỗi lượt vào `starter_v0/transcripts/ui_<id>.transcript.json`.
- **Gửi/đăng:** UI dừng để xem bản nháp, đích Telegram và bấm xác nhận hoặc hủy. Khi thiếu Telegram token/chat ID, nút thực hiện bị khóa. Hủy không gọi mạng. Xác nhận được ghi thành một lượt riêng trong transcript.

Ví dụ: “Tìm 3 tin AI trong tuần qua, kèm nguồn”; “Lấy 3 bài mới nhất của @sama”; “Đọc bài này giúp mình” rồi bổ sung URL; “Định dạng những kết quả vừa tìm thành bản tin”.

## Tích hợp phần các thành viên

| Thành viên/phần việc | Cách thử trên UI |
|---|---|
| P1 — prompt | Chọn system_prompt.md hoặc snapshot prompt mới trong artifacts, tạo phiên mới. |
| P2 — declaration | Chọn tools.yaml hoặc tools_baseline.yaml; tạo hai phiên có cùng model/prompt để quan sát khác biệt. |
| P3/P4 — tool mới | Thêm tool.py, TOOL.md, registry và YAML theo contract; chạy pytest, khởi động lại server, tạo phiên mới. Không cần thêm nút riêng trong app.py. |
| P4 — eval | Dùng câu hỏi trong eval để khám phá lỗi; điểm chính thức vẫn chạy run_eval.py. |
| P5 — UI/demo | Dùng app.py làm nền UI chung, bổ sung cách trình bày/demo nếu cần; giữ transcript và ghi link triển khai thật vào A1. |

Mặc định UI chọn `v4`; snapshot prompt và declaration cho từng version được giữ trong `artifacts/agent_versions/`. Chọn **Tùy chỉnh** để dùng các file prompt/tool tùy ý trong `artifacts/`, gồm `system_prompt_ui.md` dành cho demo nhiều bước (không phải prompt đã đo của nhóm). Model vẫn có thể chọn sai tool; UI hiển thị lỗi để nhóm phân tích, không tự đổi tool call nhằm làm đẹp kết quả.

UI dùng lại `chat.run_model_tool_loop`, thêm executor riêng để kiểm tra schema và chặn hành động chờ xác nhận. CLI vẫn dùng executor mặc định; `agent.py`/`run_eval.py` không đổi. Transcript có `origin=streamlit`, `ui_confirmation_guard=true`, model, prompt/tools hash, snapshot, rounds và tool_events. Vì guard và vòng lặp khác eval một bước, không dùng transcript UI thay cho metric eval hoặc yêu cầu chạy `chat.py` trong đề.

Prompt/declaration được giữ cố định trong phiên; code tool chạy từ registry hiện tại. Sau khi ghép code mới, khởi động lại và tạo phiên mới. Khi tải lại tab, phiên chat có thể được tạo lại; transcript cũ vẫn ở server. UI chưa hỗ trợ khôi phục phiên cũ từ JSON.

Các cấu hình `v0`–`v4` là snapshot để thử trực tiếp trong chatbot. Tab **Phiên bản Agent** cho biết fingerprint snapshot có khớp run eval đã lưu hay không; các kết quả accuracy chỉ là số liệu tham khảo từ eval, không bảo đảm UI chat có kết quả tương tự. `v0`, `v1` declaration và `v3` hiện có snapshot khôi phục không trùng hoàn toàn fingerprint lịch sử, nên không được xem là bản tái lập chính xác của run tương ứng.

## Kiểm tra

```powershell
# Offline; không gọi API:
.\.venv\Scripts\python.exe -m pytest -q
# Tự nguyện chạy live UI, dùng OpenAI/Firecrawl và quota thật:
.\.venv\Scripts\python.exe scripts/smoke_ui.py
```

Test UI dùng Streamlit AppTest để kiểm tra widget/chat/tạo phiên. Test runtime kiểm tra xác nhận một lần, hủy, đổi đích, args sai, tool mới, hội thoại nhiều lượt và lưu lỗi có che secret. Không gửi Telegram thật trong smoke test.

## Link dùng thử cho cả nhóm

App hiện được phục vụ qua một **Cloudflare Quick Tunnel tạm thời**: https://perfectly-sell-sector-enormous.trycloudflare.com. Link chỉ dùng được khi tiến trình Streamlit và tunnel còn chạy; localhost vẫn chỉ truy cập trên máy chủ. Khi link hết hạn, khởi động lại Streamlit và chạy tunnel như sau:

```powershell
cloudflared tunnel --url http://127.0.0.1:8501
```

Người có link sẽ gọi API bằng key trên máy chủ và dùng quota của chủ key; app hiện không có đăng nhập/phân quyền. Chỉ chia sẻ phạm vi nhóm tin cậy, không đưa `.env` lên GitHub. Để triển khai công khai lâu dài cần bổ sung xác thực, giới hạn sử dụng và lưu trữ phiên phù hợp. Quick Tunnel có thể đổi URL khi khởi động lại; cập nhật URL trong tài liệu/báo cáo khi cần.
