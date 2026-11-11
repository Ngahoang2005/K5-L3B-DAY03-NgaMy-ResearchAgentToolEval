"""Session-scoped UI orchestration; CLI/eval behavior remains unchanged."""
from __future__ import annotations

import copy
import json
import os
import re
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator

from chat import run_model_tool_loop, trim_history
from providers.base import ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).resolve().parent


def timestamp() -> str:
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds")


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if not isinstance(value, str):
        return value
    for key, secret in os.environ.items():
        if any(word in key.upper() for word in ("KEY", "TOKEN", "SECRET", "PASSWORD")) and len(secret) >= 6:
            value = value.replace(secret, "[REDACTED]")
    return re.sub(r"https://api\.telegram\.org/bot[^/\s]+", "https://api.telegram.org/bot[REDACTED]", value)


def tool_metadata() -> dict[str, dict[str, Any]]:
    result = {}
    for path in (ROOT / "tools").glob("*/TOOL.md"):
        try:
            text = path.read_text(encoding="utf-8")
            meta = yaml.safe_load(text.split("---", 2)[1]) if text.startswith("---") else {}
            if isinstance(meta, dict) and meta.get("name"):
                result[meta["name"]] = meta
        except (ValueError, IndexError, yaml.YAMLError):
            continue
    return result


def new_session(provider: str, model: str, version: str, prompt: Path, tools: Path,
                rounds: int = 5, history_window: int = 8) -> dict[str, Any]:
    declarations = load_tool_declarations(tools)
    names = [d["name"] for d in declarations]
    if len(names) != len(set(names)):
        raise ValueError("Tên tool bị trùng trong declaration.")
    missing = set(names) - TOOL_FUNCTIONS.keys()
    if missing:
        raise ValueError(f"Tool chưa đăng ký implementation: {', '.join(sorted(missing))}")
    for declaration in declarations:
        Draft7Validator.check_schema(declaration.get("parameters", {}))
    version_info = artifact_version_dict(build_artifact_version(version, prompt, tools))
    return {
        "transcript_id": f"ui_{uuid.uuid4().hex}", **version_info,
        "origin": "streamlit", "provider": provider, "model": model,
        "system_prompt": str(prompt.relative_to(ROOT)), "tools": str(tools.relative_to(ROOT)),
        "prompt_snapshot": prompt.read_text(encoding="utf-8"),
        "declarations_snapshot": declarations, "metadata_snapshot": tool_metadata(),
        "ui_confirmation_guard": True, "max_tool_rounds": rounds,
        "history_window": history_window, "created_at": timestamp(),
        "turns": [], "history": [], "pending": None,
    }


def call_event(session: dict[str, Any], call: ToolCall, *, approved: bool = False) -> dict[str, Any]:
    event: dict[str, Any] = {"tool": call.name, "args": copy.deepcopy(call.args)}
    declaration = next((d for d in session["declarations_snapshot"] if d["name"] == call.name), None)
    if declaration is None or call.name not in TOOL_FUNCTIONS:
        event["result"] = {"error": "unknown_tool", "message": "Tool không có trong cấu hình phiên này."}
        return event
    errors = list(Draft7Validator(declaration.get("parameters", {})).iter_errors(call.args))
    if errors:
        event["result"] = {"error": "invalid_arguments", "message": redact(errors[0].message)}
        return event
    meta = session["metadata_snapshot"].get(call.name, {})
    # Missing metadata is conservative: new tools must declare their side effects.
    action = (meta.get("side_effect") not in (False, "local_file_write")
              or meta.get("kind") == "action" or meta.get("requires_confirmation") is True
              or call.name == "send")
    if action and not approved:
        session["pending"] = {"name": call.name, "args": copy.deepcopy(call.args),
                              "destination": os.getenv("TELEGRAM_CHAT_ID", "") if call.name == "send" else ""}
        event["result"] = {"status": "pending_approval", "awaiting_user": True,
                           "question": "Bản nháp đã sẵn sàng. Hãy xem nội dung và xác nhận ở khung bên dưới; chưa có hành động nào được thực hiện."}
        return event
    try:
        event["result"] = TOOL_FUNCTIONS[call.name](**call.args)
    except Exception as exc:
        event["result"] = {"error": type(exc).__name__, "message": redact(str(exc))}
    return redact(event)


def run_turn(session: dict[str, Any], user_text: str, provider: Any) -> dict[str, Any]:
    if session["pending"]:
        raise ValueError("Xác nhận hoặc hủy hành động đang chờ trước khi gửi yêu cầu mới.")
    start = time.monotonic()
    record: dict[str, Any] = {
        "turn_index": len(session["turns"]) + 1,
        "user": user_text,
        "version": session["version"],
        "artifact_version": session["artifact_version"],
        "started_at": timestamp(),
        "rounds": [],
        "tool_events": [],
    }
    observed: list[dict[str, Any]] = []

    def execute(call: ToolCall) -> dict[str, Any]:
        event = call_event(session, call)
        observed.append(event)
        return event

    try:
        record.update(run_model_tool_loop(
            provider=provider,
            messages=[{"role": "system", "content": session["prompt_snapshot"]},
                      *trim_history(session["history"], session["history_window"]),
                      {"role": "user", "content": user_text}],
            tools=to_openai_tools(session["declarations_snapshot"]), model=session["model"] or None,
            max_tool_rounds=session["max_tool_rounds"], executor=execute, verbose=False,
        ))
    except Exception as exc:
        record.update(status="provider_error", error=redact(str(exc)),
                      assistant_text="Không hoàn tất được yêu cầu. Xem chi tiết lỗi bên dưới và thử lại sau.",
                      tool_events=observed)
    record.update(ended_at=timestamp(), duration_seconds=round(time.monotonic() - start, 2))
    session["turns"].append(redact(record))
    # Include tool evidence in future turns, so follow-ups can use retrieved items.
    context = record.get("assistant_text", "")
    if record["tool_events"]:
        context += "\nTOOL_RESULTS_JSON:\n" + json.dumps(record["tool_events"], ensure_ascii=False, default=str)[:24000]
    session["history"].extend([{"role": "user", "content": user_text}, {"role": "assistant", "content": redact(context)}])
    return record


def resolve_action(session: dict[str, Any], approve: bool) -> dict[str, Any]:
    pending = session.get("pending")
    if not pending:
        raise ValueError("Không có hành động chờ xác nhận.")
    # Consume before execution: Streamlit reruns cannot send the same action twice.
    session["pending"] = None
    if approve:
        args = copy.deepcopy(pending["args"])
        if pending["name"] == "send":
            if pending["destination"] != os.getenv("TELEGRAM_CHAT_ID", ""):
                raise ValueError("Đích Telegram đã thay đổi. Hãy tạo yêu cầu gửi mới để xác nhận lại.")
            args["confirmed"] = True
        event = call_event(session, ToolCall(pending["name"], args), approved=True)
        result = event.get("result", {})
        failed = isinstance(result, dict) and (result.get("error") or result.get("status") == "needs_confirmation")
        status = "action_error" if failed else "action_executed"
        answer = "Thao tác gặp lỗi; xem kết quả tool." if failed else "Đã thực hiện thao tác. Kết quả tool được lưu bên dưới."
    else:
        event = {"tool": pending["name"], "args": pending["args"], "result": {"status": "cancelled"}}
        status, answer = "action_cancelled", "Đã hủy. Không thực hiện thao tác."
    record = {
        "turn_index": len(session["turns"]) + 1,
        "user": "[UI] Xác nhận thực hiện" if approve else "[UI] Hủy thao tác",
        "version": session["version"],
        "artifact_version": session["artifact_version"],
        "started_at": timestamp(),
        "ended_at": timestamp(),
        "status": status,
        "assistant_text": answer,
        "rounds": [],
        "tool_events": [event],
        "duration_seconds": 0,
    }
    session["turns"].append(redact(record))
    session["history"].extend([{"role": "user", "content": record["user"]},
                                {"role": "assistant", "content": answer + "\n" + json.dumps(redact(event), ensure_ascii=False)}])
    return record


def transcript_json(session: dict[str, Any]) -> str:
    payload = {k: v for k, v in session.items() if k not in ("history", "pending")}
    payload["updated_at"] = timestamp()
    payload["pending_action"] = session.get("pending")
    return json.dumps(redact(payload), ensure_ascii=False, indent=2, default=str)


def save_session(session: dict[str, Any], folder: Path | None = None) -> Path:
    folder = folder or ROOT / "transcripts"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{session['transcript_id']}.transcript.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(transcript_json(session), encoding="utf-8")
    temporary.replace(target)
    return target
