# Bằng chứng kiểm tra — P2

Ngày thực hiện: 2026-11-10 (GMT+7). Python 3.14.4; dependency trong `starter_v0/.venv` từ requirements.

## Offline

Lệnh chạy từ `starter_v0` sau khi sửa mô tả 10 tool:

```powershell
.venv/Scripts/python.exe -m pytest -q -r s
```

Trích output thực tế:

```text
..............................................................ssssssssss [ 91%]
sssssss                                                                  [100%]
62 passed, 17 skipped in 0.37s
```

17 skip là TODO CP3 trong `tests/test_tools_todo.py`, tại dòng 26, 33, 38, 43, 51, 55, 62, 70, 74, 82, 87, 93, 98, 104, 114, 118, 122. Contract và example tests pass. Test offline không thay cho eval model và không dùng làm metric trong version_log.

## Provider thật

Người dùng cấu hình `OPENAI_API_KEY` (không phải OpenRouter). Đã chạy `scripts/preflight_provider.py --provider openai` bằng Python trong `.venv`, kết quả:

```text
OK provider=openai model=gpt-4o-mini
tool=timeline
args={'screenname': 'sama'}
```

Preflight xác minh model trả structured tool call, không thực thi timeline. Tavily, Firecrawl và RapidAPI chưa được cấu hình tại lần kiểm tra; chưa có run v2. Không lưu giá trị key vào bằng chứng.

## Firecrawl th?t

Sau khi ng??i d?ng ?i?n FIRECRAWL_API_KEY, ?? g?i tool fetch qua TOOL_FUNCTIONS v?i URL https://example.com. K?t qu?: PASS, tr? 1 item c? summary kh?ng r?ng, kh?ng c? l?i HTTP. ??y l? smoke test k?t n?i/tool, kh?ng ph?i eval routing v2. Kh?ng l?u key.

## RapidAPI v? Tavily th?t

Sau khi ng??i d?ng b? sung key, social_search(query="OpenAI", search_type="Latest", limit=1) PASS v?i 1 item. Timeline(screenname="sama", limit=1) l?i ? l?n ??u (kh?ng ghi nh?n m? HTTP), th? l?i PASS v?i 1 item; ch?a x?c ??nh nguy?n nh?n ban ??u. Lookup(query="AI research", max_results=1) PASS v?i 1 item. C? b?n d?ch v? OpenAI, Firecrawl, Tavily v? RapidAPI ?? c? smoke test th?nh c?ng; ch?a thay th? run eval v2.
