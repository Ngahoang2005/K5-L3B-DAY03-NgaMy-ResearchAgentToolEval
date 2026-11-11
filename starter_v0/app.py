"""Run: python -m streamlit run app.py"""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from agent_versions import AGENT_VERSIONS, version_diff
from env_loader import load_lab_env
from providers import make_provider
from ui_runtime import ROOT, new_session, redact, resolve_action, run_turn, save_session, transcript_json
from versioning import build_artifact_version

st.set_page_config(page_title="NgaMy Research", page_icon="🔎", layout="wide")
load_lab_env(ROOT)

st.markdown("""<style>
.stApp {background: #f7f8fc;}
.block-container {max-width: 1180px; padding-top: 4rem; padding-bottom: 6rem;}
[data-testid="stBottomBlockContainer"] {padding-bottom: .75rem !important;}
[data-testid="stBottom"] {position: fixed !important; bottom: 0; z-index: 999;}
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
    version_choices = [*AGENT_VERSIONS, "Tùy chỉnh"]
    selected_version = st.selectbox("Version agent", version_choices, index=version_choices.index("v4"))
    if selected_version == "Tùy chỉnh":
        version = st.text_input("Nhãn phiên tùy chỉnh", value="ui-preview")
        prompt_names = sorted(path.name for path in (ROOT / "artifacts").glob("*.md"))
        selected_prompt = st.selectbox(
            "System prompt",
            prompt_names,
            index=prompt_names.index("system_prompt.md") if "system_prompt.md" in prompt_names else 0,
        )
        tool_names = sorted(path.name for path in (ROOT / "artifacts").glob("*.yaml"))
        selected_tools = st.selectbox(
            "Tool declaration",
            tool_names,
            index=tool_names.index("tools.yaml") if "tools.yaml" in tool_names else 0,
        )
        prompt_path = ROOT / "artifacts" / selected_prompt
        tools_path = ROOT / "artifacts" / selected_tools
        version = version.strip() or "ui-preview"
    else:
        profile = AGENT_VERSIONS[selected_version]
        prompt_path = profile.prompt_path
        tools_path = profile.tools_path
        version = profile.version
        st.caption(f"{profile.title} · Eval tham khảo: {profile.accuracy}")
    with st.expander("Giới hạn hội thoại"):
        rounds = st.slider("Vòng tool tối đa mỗi lượt", 1, 10, 5)
        history_window = st.slider("Số cặp hội thoại giữ trong ngữ cảnh", 1, 20, 8)
    apply = st.button("Áp dụng version & tạo phiên mới", type="primary", width="stretch")
    st.caption("Đổi cấu hình cần tạo phiên mới. Phiên cũ đã tự lưu sau mỗi lượt; tải JSON trước khi đổi nếu cần.")
    if apply or "research" not in st.session_state:
        try:
            st.session_state.research = new_session(provider_name, model.strip() or default_model,
                version, prompt_path, tools_path, rounds, history_window)
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

st.markdown('<div class="eyebrow">RESEARCH WORKSPACE / NGAMY</div><div class="hero">Từ câu hỏi đến nguồn tin.</div><div class="subtitle">Tra cứu, kiểm chứng và tổng hợp — cùng một nơi để cả nhóm thử agent.</div>', unsafe_allow_html=True)
top = st.columns(3)
top[0].metric("Model đang dùng", session["model"])
top[1].metric("Tool sẵn sàng", len(session["declarations_snapshot"]))
top[2].metric("Lượt hội thoại", len(session["turns"]))
st.caption(f"Phiên: {session['version']} · {session['provider']} · Prompt: {session['system_prompt']} · Tools: {session['tools']}")
chat_tab, tools_tab, versions_tab, history_tab = st.tabs(
    ["Trò chuyện", "Công cụ & cấu hình", "Phiên bản Agent", "Lịch sử chat"],
    key="research_tabs",
    on_change="rerun",
)

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

with versions_tab:
    st.subheader("Phiên bản Agent")
    st.caption(f"Đang xem: **{selected_version}** · Phiên chatbot đang chạy: **{session['version']}**.")
    if selected_version == "Tùy chỉnh":
        st.info("Cấu hình tùy chỉnh không có lịch sử version để so sánh. Chọn v0–v4 ở thanh bên để xem thay đổi.")
    else:
        selected_profile = AGENT_VERSIONS[selected_version]
        st.markdown(f"**{selected_profile.title}** · Độ chính xác eval tham khảo: **{selected_profile.accuracy}**")
        for change in selected_profile.changes:
            st.markdown(f"- {change}")
        st.caption(selected_profile.source)
        candidate_version = build_artifact_version(
            selected_profile.version, selected_profile.prompt_path, selected_profile.tools_path,
        )
        st.caption("Fingerprint snapshot được áp dụng:")
        st.code(candidate_version.artifact_version, language=None)
        if (candidate_version.prompt_hash[:12] != selected_profile.prompt_hash
                or candidate_version.tools_hash[:12] != selected_profile.tools_hash):
            st.warning("Snapshot này không trùng hoàn toàn fingerprint của run eval lịch sử; transcript sẽ ghi fingerprint thực tế ở trên.")
        if selected_version != "v0":
            st.code(version_diff(selected_version), language="diff")

with history_tab:
    st.subheader("Lịch sử chat")
    st.info("UI dùng vòng chat nhiều bước và có nút xác nhận hành động. Transcript UI không thay thế run_eval.py hoặc yêu cầu chạy chat.py trong đề.")
    st.code(session["artifact_version"], language=None)
    st.caption("Prompt/declaration được chụp lại khi tạo phiên để các lượt dùng cùng cấu hình.")
    st.write(f"File tự lưu: transcripts/{session['transcript_id']}.transcript.json")
    if session["turns"]:
        st.dataframe([{"Lượt": t["turn_index"], "Version agent": t.get("version", session["version"]),
                       "Artifact version": t.get("artifact_version", session["artifact_version"]),
                       "Yêu cầu": t["user"], "Trạng thái": t["status"],
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
            turn_version = turn.get("version", session["version"])
            turn_artifact_version = turn.get("artifact_version", session["artifact_version"])
            st.caption(
                f"Agent {turn_version} · {turn_artifact_version} · "
                f"{turn['status']} · {turn.get('duration_seconds', 0)} giây"
            )
            if turn.get("error"):
                st.error(turn["error"])
            for index, event in enumerate(turn.get("tool_events", []), 1):
                result = event.get("result", {})
                failed = isinstance(result, dict) and bool(result.get("error"))
                with st.expander(f"{'⚠' if failed else '↳'} {event['tool']} · kết quả {index}"):
                    st.json(event)
    if chat_tab.open:
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


if chat_tab.open:
    user_text = st.chat_input("Hỏi về tin tức, gửi URL hoặc tiếp tục câu hỏi…", disabled=bool(session.get("pending")), max_chars=12000)
    if user_text:
        with st.spinner("Đang tìm nguồn và xử lý yêu cầu…"):
            run_turn(session, user_text, make_provider(session["provider"]))
            persist()
        st.rerun()
