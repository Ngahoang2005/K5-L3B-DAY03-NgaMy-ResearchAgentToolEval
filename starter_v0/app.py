"""Run: python -m streamlit run app.py"""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from ui_runtime import ROOT, new_session, redact, resolve_action, run_turn, save_session, transcript_json

st.set_page_config(page_title="NgaMy Research", page_icon="🔎", layout="wide")
load_lab_env(ROOT)

st.markdown("""<style>
.stApp {background: #f7f8fc;}
.block-container {max-width: 1180px; padding-top: 4rem;}
[data-testid="stBottomBlockContainer"] {padding-bottom: .75rem !important;}
[data-testid="stSidebar"] {background: #eef1f8;}
[data-testid="stChatMessage"] {border: 1px solid #e3e8f1; border-radius: 16px; background: white;}
.eyebrow {color: #5367b2; font-size: .75rem; font-weight: 700; letter-spacing: .18em; margin-bottom: .4rem;}
.hero {font-size: 2.5rem; font-weight: 750; letter-spacing: -.06em; color: #17233c; line-height: 1.15;}
.subtitle {color: #64748b; margin: .8rem 0 1.5rem;}
</style>""", unsafe_allow_html=True)


def persist() -> None:
    try:
        save_session(st.session_state.research)
        st.session_state.save_error = None
    except OSError as exc:
        st.session_state.save_error = redact(str(exc))


with st.sidebar:
    st.markdown("### 🔎 NgaMy Research")
    st.caption("Tìm nguồn · Đọc sâu · Tổng hợp")
    st.divider()
    st.markdown("**Cấu hình phiên**")
    provider_name = st.selectbox("Provider", ["openai", "openrouter", "anthropic", "gemini", "ollama"], key="provider_choice")
    default_model = getattr(make_provider(provider_name), "default_model", "")
    model = st.text_input("Model (để trống dùng mặc định)", placeholder=default_model, key=f"model_{provider_name}")
    version = st.text_input("Nhãn phiên", value="ui-preview", help="Nhãn ghi vào transcript; không tự tạo một run eval v2.")
    prompts = sorted((ROOT / "artifacts").glob("*.md"))
    prompt_names = [p.name for p in prompts]
    # Default to the measured project prompt (v1, used by v2 eval); system_prompt_ui.md stays selectable for demos.
    selected_prompt = st.selectbox("System prompt", prompt_names, index=prompt_names.index("system_prompt.md") if "system_prompt.md" in prompt_names else 0)
    tool_paths = sorted((ROOT / "artifacts").glob("*.yaml"))
    tool_names = [p.name for p in tool_paths]
    selected_tools = st.selectbox("Tool declaration", tool_names, index=tool_names.index("tools.yaml") if "tools.yaml" in tool_names else 0)
    with st.expander("Giới hạn hội thoại"):
        rounds = st.slider("Vòng tool tối đa mỗi lượt", 1, 10, 5)
        history_window = st.slider("Số cặp hội thoại giữ trong ngữ cảnh", 1, 20, 8)
    apply = st.button("Áp dụng & tạo phiên mới", type="primary", width="stretch")
    st.caption("Đổi cấu hình cần tạo phiên mới. Phiên cũ đã tự lưu sau mỗi lượt; tải JSON trước khi đổi nếu cần.")
    if apply or "research" not in st.session_state:
        try:
            st.session_state.research = new_session(provider_name, model.strip() or default_model,
                version.strip() or "ui-preview", ROOT / "artifacts" / selected_prompt,
                ROOT / "artifacts" / selected_tools, rounds, history_window)
            st.session_state.save_error = None
        except Exception as exc:
            st.error(redact(str(exc)))
    if "research" not in st.session_state:
        st.stop()
    session = st.session_state.research
    st.divider()
    st.markdown("**Kết nối trên máy chủ**")
    provider_env = {"openai": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "gemini": "GEMINI_API_KEY"}
    for label, key in [("Model", provider_env.get(session["provider"], "")), ("Tavily", "TAVILY_API_KEY"), ("Firecrawl", "FIRECRAWL_API_KEY"), ("RapidAPI", "RAPIDAPI_KEY")]:
        ready = bool(os.getenv(key)) if key else True
        st.caption(f"{'●' if ready else '○'} {label} — {'đã cấu hình' if ready else 'chưa có key'}")
    st.caption("Trạng thái cấu hình không thay thế kiểm tra kết nối. Key chỉ đọc từ .env trên máy chủ.")
    st.download_button("↓ Tải transcript JSON", transcript_json(session),
        file_name=f"{session['transcript_id']}.transcript.json", mime="application/json", width="stretch")

if "chat_started" not in st.session_state:
    st.session_state.chat_started = bool(session["turns"])
chat_input_position = "sticky" if st.session_state.chat_started else "static"
st.markdown(f"""<style>
[data-testid="stBottom"] {{position: {chat_input_position} !important; bottom: 0;}}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="eyebrow">RESEARCH WORKSPACE / NGAMY</div><div class="hero">Từ câu hỏi đến nguồn tin.</div><div class="subtitle">Tra cứu, kiểm chứng và tổng hợp — cùng một nơi để cả nhóm thử agent.</div>', unsafe_allow_html=True)
top = st.columns(3)
top[0].metric("Model đang dùng", session["model"])
top[1].metric("Tool sẵn sàng", len(session["declarations_snapshot"]))
top[2].metric("Lượt hội thoại", len(session["turns"]))
st.caption(f"Phiên: {session['version']} · {session['provider']} · Prompt: {session['system_prompt']} · Tools: {session['tools']}")
chat_tab, tools_tab, evidence_tab = st.tabs(["Chat", "Công cụ & cấu hình", "Lịch sử chat"])

with tools_tab:
    st.subheader("Bộ công cụ của phiên này")
    st.caption("Đọc tự động từ YAML và registry. Sau khi thêm tool/code mới, khởi động lại server và tạo phiên mới để dùng bản mới nhất.")
    for declaration in session["declarations_snapshot"]:
        name = declaration["name"]
        meta = session["metadata_snapshot"].get(name, {})
        with st.expander(name):
            st.write(declaration.get("description", ""))
            st.caption(f"Loại: {meta.get('kind', 'chưa có metadata')} · Side effect: {meta.get('side_effect', 'chưa khai báo')}")
            requirements = meta.get("requires_env", [])
            if requirements:
                st.write("Biến môi trường: " + ", ".join(f"{key} ({'đã có' if os.getenv(key) else 'chưa có'})" for key in requirements))
            st.json(declaration.get("parameters", {}))
    with st.expander("System prompt đang sử dụng"):
        st.code(session["prompt_snapshot"], language="markdown")

with evidence_tab:
    st.subheader("Lịch sử chat")
    st.info("UI dùng vòng chat nhiều bước và có nút xác nhận hành động. Transcript UI không thay thế run_eval.py hoặc yêu cầu chạy chat.py trong đề.")
    st.code(session["artifact_version"], language=None)
    st.caption("Prompt/declaration được chụp lại khi tạo phiên để các lượt dùng cùng cấu hình.")
    st.write(f"File tự lưu: transcripts/{session['transcript_id']}.transcript.json")
    if session["turns"]:
        st.dataframe([{"Lượt": t["turn_index"], "Yêu cầu": t["user"], "Trạng thái": t["status"],
                       "Số tool": len(t["tool_events"]), "Giây": t.get("duration_seconds", 0)} for t in session["turns"]],
                     width="stretch", hide_index=True)
    else:
        st.caption("Lịch sử phiên chat sẽ được lưu lại ở đây.")

with chat_tab:
    if not session["turns"]:
        st.subheader("Bạn muốn tìm hiểu điều gì?")
        st.caption("Thử thêm: “Đọc bài này giúp mình” để kiểm tra hỏi lại, hoặc yêu cầu soạn bản tin để kiểm tra format.")
    for turn in session["turns"]:
        with st.chat_message("user"):
            st.write(turn["user"])
        with st.chat_message("assistant"):
            st.markdown(turn.get("assistant_text") or "Không có nội dung trả lời.")
            st.caption(f"{turn['status']} · {turn.get('duration_seconds', 0)} giây")
            if turn.get("error"):
                st.error(turn["error"])
            for index, event in enumerate(turn.get("tool_events", []), 1):
                result = event.get("result", {})
                failed = isinstance(result, dict) and bool(result.get("error"))
                with st.expander(f"{'⚠' if failed else '↳'} {event['tool']} · kết quả {index}"):
                    st.json(event)
    if session.get("pending"):
        pending = session["pending"]
        with st.container(border=True):
            st.subheader("Xác nhận thao tác")
            st.write(f"Tool: **{pending['name']}**")
            if pending["name"] == "send":
                st.write("Đích Telegram: " + (pending["destination"] or "Chưa cấu hình TELEGRAM_CHAT_ID"))
                st.text(pending["args"].get("text", ""))
            else:
                st.json(redact(pending["args"]))
            ready = pending["name"] != "send" or bool(os.getenv("TELEGRAM_BOT_TOKEN") and pending["destination"])
            if not ready:
                st.warning("Cần TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID để gửi thật. Bạn có thể hủy bản nháp này.")
            yes, no = st.columns(2)
            approved = yes.button("Xác nhận thực hiện", disabled=not ready, type="primary", width="stretch")
            cancelled = no.button("Hủy thao tác", width="stretch")
            if approved or cancelled:
                try:
                    with st.spinner("Đang xử lý…"):
                        resolve_action(session, approved)
                except Exception as exc:
                    st.error(redact(str(exc)))
                persist()
                st.rerun()
    if st.session_state.get("save_error"):
        st.error("Chưa lưu được transcript: " + st.session_state.save_error + ". Hãy tải JSON từ thanh bên.")

user_text = st.chat_input("Hỏi về tin tức, gửi URL hoặc tiếp tục câu hỏi…", disabled=bool(session.get("pending")), max_chars=12000)
if user_text:
    st.session_state.chat_started = True
    with st.spinner("Đang tìm nguồn và xử lý yêu cầu…"):
        run_turn(session, user_text, make_provider(session["provider"]))
        persist()
    st.rerun()
