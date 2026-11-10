# P2 — Hướng dẫn chạy và bàn giao cho Huyền

## Trạng thái

Đã chuẩn bị tool declaration v2 cho 10 tool có sẵn và môi trường `.venv`.
OpenAI key đã được người dùng cấu hình; preflight `--provider openai` PASS với `gpt-4o-mini`. Ba key Tavily/Firecrawl/RapidAPI còn trống tại lần kiểm tra. Chưa chạy v2: thiếu prompt v1 và run v1 của P1.
Chưa chạy bonus: chưa có Ollama và bản v3 đã đo của nhóm.
`RULES.md` và `RUBRIC.md` được README liên kết nhưng không có trong checkout hiện tại; cần bổ sung để đối chiếu rubric đầy đủ.

## Điền API key

**Cấu hình hiện tại dùng OpenAI:** giữ `OPENAI_API_KEY` đã điền, không đổi tên key này thành OpenRouter. Dùng `--provider openai` thay cho `--provider openrouter` trong các lệnh bên dưới. Không cần tạo thêm OpenRouter key nếu cả nhóm thống nhất chạy OpenAI. So sánh v1/v2 cần cùng provider/model với Nga.

Mở `starter_v0/.env` bằng VS Code. File này đã được tạo từ `.env.example` và được Git bỏ qua. Chỉ thay phần sau dấu `=` bằng key thật, không giữ chữ `DIEN_KEY_O_DAY`:

```dotenv
OPENROUTER_API_KEY=DIEN_KEY_O_DAY
TAVILY_API_KEY=DIEN_KEY_O_DAY
FIRECRAWL_API_KEY=DIEN_KEY_O_DAY
RAPIDAPI_KEY=DIEN_KEY_O_DAY
RAPIDAPI_TWITTER_HOST=twitter-api45.p.rapidapi.com
```

1. OpenRouter: đăng nhập [trang API keys](https://openrouter.ai/settings/keys), tạo key, sao chép vào `OPENROUTER_API_KEY`. Dùng cùng model với Nga khi so sánh v1/v2; tài khoản cần đủ quyền/quota cho model đó. [Tài liệu](https://openrouter.ai/docs/quickstart).
2. Tavily: đăng nhập [dashboard](https://app.tavily.com), tạo/sao chép API key vào `TAVILY_API_KEY`. [Tài liệu](https://docs.tavily.com/).
3. Firecrawl: đăng nhập [Firecrawl](https://www.firecrawl.dev), lấy API key của tài khoản vào `FIRECRAWL_API_KEY`. Code hiện tại của repo yêu cầu key. [Tài liệu](https://docs.firecrawl.dev/introduction).
4. RapidAPI: mở [Twitter API45](https://rapidapi.com/alexanderxbx/api/twitter-api45), đăng ký gói phù hợp và lấy `X-RapidAPI-Key` của app vào `RAPIDAPI_KEY`. Giữ đúng host ở trên. Có key nhưng chưa đăng ký API vẫn có thể bị từ chối. [Tài liệu về key](https://docs.rapidapi.com/v2/docs/keys-and-key-rotation).

Không đưa key vào chat, báo cáo hay commit. Xem giá/quota thực tế trên dashboard; không coi số quota cũ trong đề là cam kết hiện hành. Không cần Telegram token cho phần P2. Ollama không cần model API key, nhưng các tool web vẫn gọi dịch vụ ngoài và cần key riêng.

Từ thư mục gốc project, mở terminal PowerShell:

```powershell
cd starter_v0
.\.venv\Scripts\python.exe scripts/preflight_provider.py --provider openrouter
.\.venv\Scripts\python.exe -m pytest -q
```

Không cần Activate.ps1. Khi chuyển sang máy mới, tạo môi trường trước:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Preflight chỉ xác minh provider; vẫn cần xem `tool_results` để phát hiện lỗi API của từng tool. Không kết luận tool hoạt động chỉ từ điểm routing.

## Phối hợp với Nga để đo v2

Không cần đợi Nga push để viết mô tả và chạy unit test. Để đo v2 đúng thứ tự, cần Nga bàn giao:

- Prompt v1 thực tế và tool declaration đã dùng cho v1.
- Run JSON v0/v1 hợp lệ, provider/model, dòng version log tương ứng.
- Các lỗi v1 để kiểm tra giả thuyết P2.

Nga có thể push commit/branch hoặc chuyển các file; không bắt buộc push mới làm được. Không ghi đè thay đổi chưa commit khi lấy phần của Nga.

`artifacts/tools_baseline.yaml` là bản sao nguyên byte của tools.yaml starter trước khi P2 sửa. Nếu P1 chưa chạy v0, dùng bản này với prompt starter chưa sửa. Khi chạy v1, P1 chỉ đổi prompt, vẫn dùng tool baseline:

```powershell
# Chỉ chạy khi system_prompt.md vẫn là prompt starter cho v0.
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --version v0 --suite base --tools artifacts/tools_baseline.yaml --eval-cases data/eval_base.json
# P1 sửa prompt cho v1 rồi chạy:
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --version v1 --suite base --tools artifacts/tools_baseline.yaml --eval-cases data/eval_base.json
# Giữ nguyên chính prompt v1, P2 chạy candidate tools.yaml:
.\.venv\Scripts\python.exe run_eval.py --provider openrouter --version v2 --suite base --tools artifacts/tools.yaml --eval-cases data/eval_base.json
```

Nếu Nga dùng model cụ thể, thêm `--model TEN_MODEL_CUA_NGA` vào các lệnh tương ứng. Nếu tools v1 của Nga khác bản baseline đã lưu, cần đối chiếu lại trước khi đo. Khi P3/P4 thêm tool, không thay tập tool giữa hai run so sánh mà không ghi rõ ảnh hưởng.

Giả thuyết v2: làm rõ phạm vi sử dụng/không sử dụng và quy ước tham số trong tool declaration sẽ giảm lỗi routing/args so với v1, khi giữ nguyên prompt, model và bộ base. Đây là một giả thuyết ở mức toàn bộ declaration; muốn xác định đóng góp từng mô tả phải có các run bổ sung riêng.

Sau khi chạy thật:

1. Chỉ nhận run có `provider_error_cases == 0` và `measured_cases == total_cases`.
2. Kiểm tra `prompt_hash` v1/v2 giống nhau, `tools_hash` khác nhau; cùng provider/model/bộ case.
3. So `case_accuracy`, `tool_routing_accuracy`, `argument_accuracy`, `multiturn_accuracy` và đọc các case thay đổi PASS/FAIL.
4. Ghi dòng v2 vào `artifacts/version_log.csv` đúng các cột có sẵn; copy hash và artifact_version từ run JSON, không tự điền số giả.
5. Cập nhật B1, kết luận cá nhân và dẫn run thật. Nếu điểm không tăng, vẫn báo đúng kết quả và phân tích nguyên nhân.

## Bonus Ollama (sau khi có v3)

1. Tải bộ cài Windows từ [Ollama](https://ollama.com/download/windows), cài và mở ứng dụng, rồi mở terminal mới.
2. Kiểm tra `ollama --version`; chạy `ollama serve` nếu ứng dụng chưa phục vụ. Nếu đã chạy server, không cần chạy thêm.
3. Tải hai model mà đề gợi ý (cần nhiều GB dung lượng và thời gian):

```powershell
ollama pull qwen2.5:7b
ollama pull llama3.2:3b
ollama list
.\.venv\Scripts\python.exe scripts/preflight_provider.py --provider ollama --model qwen2.5:7b
.\.venv\Scripts\python.exe scripts/preflight_provider.py --provider ollama --model llama3.2:3b
```

Nếu máy không đủ RAM cho 7B, đánh giá lại cặp model trước khi tải. Không coi hai model cùng kích thước là đáp ứng yêu cầu hai kích thước khác nhau của đề.

Khi đã có prompt/tools v3 của nhóm, lưu snapshot rồi chạy hai baseline local với đúng snapshot đó:

```powershell
.\.venv\Scripts\python.exe run_eval.py --provider ollama --model qwen2.5:7b --version v3-qwen7b --suite base --eval-cases data/eval_base.json
.\.venv\Scripts\python.exe run_eval.py --provider ollama --model llama3.2:3b --version v3-llama3b --suite base --eval-cases data/eval_base.json
```

Đọc lỗi thật, chọn một model và làm hai vòng `v4-local`, `v5-local`, mỗi vòng một giả thuyết. Dùng bản prompt/tools riêng qua `--system-prompt` và `--tools`, giữ snapshot từng version. Sau đó chạy bản v5-local trên model cloud để kiểm tra ngược. Ghi tất cả run vào version_log và B7, so sánh routing, args, multi-turn; đếm lỗi tên tool, JSON args, bỏ clarify và gọi thừa từ log. Chưa có log thì để kết quả là chưa đo, không ghi 0% hay kết luận cải thiện.

## Tiêu chí bàn giao P2

- [x] 10 tool có mô tả dùng/không dùng và quy ước tham số.
- [x] `send` chỉ sau xác nhận, `confirmed` là boolean; thiếu thông tin dùng `clarify`.
- [x] Kiểm tra offline: 62 passed, 17 skipped (stub P3/P4), 0 failed.
- [ ] Có v1/v2 thật, so sánh và version_log.
- [ ] Có đủ bằng chứng bonus B7 nếu làm bonus.
- [ ] Bổ sung RULES.md/RUBRIC.md và đối chiếu lại.
- [ ] Huyền xem lại báo cáo, điền email nếu cần, tạo commit kỹ thuật và push phần đã hoàn thành.
