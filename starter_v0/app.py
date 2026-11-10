from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ROOT,
    json_text,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


PROVIDERS = ["openai", "openrouter", "anthropic", "gemini", "ollama"]
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"


@st.cache_resource
def get_provider(provider_name: str):
    return make_provider(provider_name)


def new_transcript(
    provider: str,
    model: str | None,
    version: str,
    history_window: int,
    max_tool_rounds: int,
) -> dict[str, Any]:
    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_version = build_artifact_version(version, system_prompt_path, tools_path)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider), timestamp])
    return {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider,
        "model": model,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def save_transcript() -> Path:
    transcript = st.session_state["transcript"]
    path = TRANSCRIPTS_DIR / f"{transcript['transcript_id']}.transcript.json"
    write_transcript(path, transcript)
    return path


def run_turn(user_text: str) -> None:
    transcript = st.session_state["transcript"]
    config = st.session_state["config"]
    system_prompt_path = Path(transcript["system_prompt"])
    tools_path = Path(transcript["tools"])
    prompt = system_prompt_path.read_text(encoding="utf-8")
    declared_tools = to_openai_tools(load_tool_declarations(tools_path))
    messages = [
        {"role": "system", "content": prompt},
        *trim_history(st.session_state["history"], config["history_window"]),
        {"role": "user", "content": user_text},
    ]
    turn: dict[str, Any] = {
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": "",
        "rounds": [],
        "tool_events": [],
    }
    try:
        result = run_model_tool_loop(
            provider=get_provider(config["provider"]),
            messages=messages,
            tools=declared_tools,
            model=config["model"],
            max_tool_rounds=config["max_tool_rounds"],
        )
        turn.update(result)
        answer = result["assistant_text"]
    except Exception as exc:
        turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
        answer = f"Lỗi khi gọi agent: {type(exc).__name__}: {exc}"

    turn["ended_at"] = now_iso()
    transcript["turns"].append(turn)
    st.session_state["history"].extend([
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": answer},
    ])
    save_transcript()


def show_tool_events(events: list[dict[str, Any]]) -> None:
    for event in events:
        with st.expander(f"Tool: {event.get('tool', 'unknown')}"):
            st.code(json_text(event), language="json")


def main() -> None:
    load_lab_env(ROOT)
    st.set_page_config(page_title="Research Agent", page_icon="🔎")
    st.title("Research Agent")
    st.caption("Nghiên cứu web, bài đăng và paper. Cần tích hợp và kiểm tra guardrail CP2 trước khi thử gửi/đăng thật.")

    with st.sidebar:
        st.header("Cấu hình phiên")
        provider_name = st.selectbox("Provider", PROVIDERS, index=0)
        model = st.text_input("Model (để trống dùng mặc định)", value="")
        version = st.text_input("Version", value="v3")
        history_window = int(st.number_input("Lượt chat trong ngữ cảnh", 1, 20, 5))
        max_tool_rounds = int(st.number_input("Vòng gọi tool tối đa", 1, 10, 4))
        new_chat = st.button("Bắt đầu phiên mới", type="primary")
        config = {
            "provider": provider_name,
            "model": model.strip() or None,
            "version": version.strip() or "v3",
            "history_window": history_window,
            "max_tool_rounds": max_tool_rounds,
        }
        if new_chat or "transcript" not in st.session_state:
            st.session_state["history"] = []
            st.session_state["transcript"] = new_transcript(**config)
            st.session_state["config"] = config
        elif st.session_state["config"] != config:
            st.info("Cấu hình thay đổi sẽ có hiệu lực khi bạn bắt đầu phiên mới.")

    transcript = st.session_state["transcript"]
    st.caption(f"{transcript['provider']} · {transcript['artifact_version']}")
    for turn in transcript["turns"]:
        with st.chat_message("user"):
            st.markdown(turn["user"])
        with st.chat_message("assistant"):
            if turn.get("status") == "provider_error":
                st.error(turn.get("error", "Provider error"))
            else:
                st.markdown(turn.get("assistant_text", ""))
            show_tool_events(turn.get("tool_events", []))

    user_text = st.chat_input("Nhập yêu cầu nghiên cứu")
    if user_text and user_text.strip():
        with st.spinner("Agent đang xử lý..."):
            run_turn(user_text.strip())
        st.rerun()

    st.caption(f"Transcript được ghi trong `{TRANSCRIPTS_DIR}`.")


if __name__ == "__main__":
    main()
