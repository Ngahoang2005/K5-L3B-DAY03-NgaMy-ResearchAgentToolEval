"""Opt-in live UI smoke test. Uses configured OpenAI/Firecrawl credits; never sends Telegram."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest


def main():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=90).run()
    assert not app.exception, "UI failed to initialize"
    next(s for s in app.selectbox if s.label == "Version agent").select("Tùy chỉnh").run()
    next(t for t in app.text_input if t.label == "Nhãn phiên tùy chỉnh").set_value("ui-smoke-live")
    next(b for b in app.button if b.label == "Áp dụng version & tạo phiên mới").click().run()
    for query in ["Đọc bài này và tóm tắt giúp mình.", "https://example.com",
                  "Trình bày nội dung vừa đọc thành 2 gạch đầu dòng, giữ nguồn."]:
        app.chat_input[0].set_value(query).run(timeout=90)
        assert not app.exception, "UI failed while processing a turn"
        turn = app.session_state.research["turns"][-1]
        print({"turn": turn["turn_index"], "status": turn["status"],
               "tools": [e["tool"] for e in turn["tool_events"]]}, flush=True)
        assert turn["status"] != "provider_error", "Provider error; inspect transcript locally"
    print("Transcript: transcripts/" + app.session_state.research["transcript_id"] + ".transcript.json")


if __name__ == "__main__":
    main()
