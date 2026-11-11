from __future__ import annotations

import json

import pytest

from agent_versions import AGENT_VERSIONS, version_diff
import ui_runtime as ui
from providers.base import ModelResponse, ToolCall


class FakeProvider:
    default_model = "test-model"

    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []

    def complete(self, messages, *args, **kwargs):
        self.messages.append(messages)
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def session():
    return ui.new_session("openai", "test-model", "ui-test", ui.ROOT / "artifacts/system_prompt_ui.md",
                          ui.ROOT / "artifacts/tools.yaml")


def test_send_requires_ui_approval_even_when_model_sets_true(session, monkeypatch):
    sent = []
    monkeypatch.setitem(ui.TOOL_FUNCTIONS, "send", lambda **args: sent.append(args) or {"status": "sent"})
    provider = FakeProvider([ModelResponse(tool_calls=[ToolCall("send", {"text": "Draft", "confirmed": True})])])
    result = ui.run_turn(session, "Send this", provider)
    assert result["status"] == "waiting_for_user"
    assert result["version"] == session["version"]
    assert result["artifact_version"] == session["artifact_version"]
    assert sent == []
    ui.resolve_action(session, True)
    assert sent == [{"text": "Draft", "confirmed": True}]
    assert session["turns"][-1]["version"] == session["version"]
    assert session["turns"][-1]["artifact_version"] == session["artifact_version"]
    with pytest.raises(ValueError):
        ui.resolve_action(session, True)
    assert len(sent) == 1


def test_cancel_does_not_execute_action(session, monkeypatch):
    def unexpected(**kwargs):
        pytest.fail("Cancelled action executed")
    monkeypatch.setitem(ui.TOOL_FUNCTIONS, "send", unexpected)
    ui.call_event(session, ToolCall("send", {"text": "Draft"}))
    assert ui.resolve_action(session, False)["status"] == "action_cancelled"
    assert session["pending"] is None


def test_changed_destination_cannot_use_previous_approval(session, monkeypatch):
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "one")
    ui.call_event(session, ToolCall("send", {"text": "Draft"}))
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "two")
    with pytest.raises(ValueError, match="Telegram"):
        ui.resolve_action(session, True)


def test_bad_args_never_reach_tool(session, monkeypatch):
    monkeypatch.setitem(ui.TOOL_FUNCTIONS, "send", lambda **kwargs: pytest.fail("Invalid args executed"))
    result = ui.call_event(session, ToolCall("send", {"text": "Draft", "confirmed": "false"}))
    assert result["result"]["error"] == "invalid_arguments"
    assert session["pending"] is None


def test_new_registered_tool_is_available_without_ui_changes(session, monkeypatch):
    session["declarations_snapshot"].append({"name": "new_team_tool", "parameters": {"type": "object"}})
    session["metadata_snapshot"]["new_team_tool"] = {"side_effect": False}
    monkeypatch.setitem(ui.TOOL_FUNCTIONS, "new_team_tool", lambda: {"value": 42})
    assert ui.call_event(session, ToolCall("new_team_tool", {}))["result"] == {"value": 42}


def test_clarification_preserves_history_and_tool_evidence(session):
    provider = FakeProvider([
        ModelResponse(tool_calls=[ToolCall("clarify", {"question": "URL nào?"})]),
        ModelResponse(text="Đã nhận URL."),
    ])
    ui.run_turn(session, "Đọc bài này", provider)
    assert session["turns"][0]["status"] == "waiting_for_user"
    ui.run_turn(session, "https://example.com", provider)
    context = str(provider.messages[-1])
    assert "Đọc bài này" in context and "URL nào?" in context and "TOOL_RESULTS_JSON" in context


def test_provider_failure_keeps_prior_tool_events_and_redacts_secrets(session, monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "private-test-secret")
    provider = FakeProvider([
        ModelResponse(tool_calls=[ToolCall("format", {"items": [], "template": "brief"})]),
        RuntimeError("failure private-test-secret"),
    ])
    ui.run_turn(session, "Format", provider)
    assert session["turns"][0]["status"] == "provider_error"
    assert len(session["turns"][0]["tool_events"]) == 1
    path = ui.save_session(session, tmp_path)
    raw = path.read_text(encoding="utf-8")
    assert "private-test-secret" not in raw
    saved = json.loads(raw)
    assert saved["prompt_hash"] == session["prompt_hash"]
    assert saved["origin"] == "streamlit"
    assert saved["turns"][0]["error"] == "failure [REDACTED]"


def test_agent_version_profiles_have_distinct_snapshots_and_change_notes():
    assert list(AGENT_VERSIONS) == ["v0", "v1", "v2", "v3", "v4"]
    sessions = {
        version: ui.new_session(
            "openai", "test-model", profile.version, profile.prompt_path, profile.tools_path
        )
        for version, profile in AGENT_VERSIONS.items()
    }
    assert [len(sessions[version]["declarations_snapshot"]) for version in AGENT_VERSIONS] == [
        10, 10, 10, 10, 14,
    ]
    assert sessions["v2"]["artifact_version"] == "v2+pea21801f0290+t64a6349a4b00"
    assert sessions["v4"]["artifact_version"] == "v4+pea21801f0290+t85fc98b68764"
    assert "clarify" in version_diff("v1")
    assert "yes_no" in version_diff("v2")
    assert "policy_area" in version_diff("v3")
    assert "wiki" in version_diff("v4")


def test_streamlit_chat_and_new_session(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    import env_loader
    import providers
    monkeypatch.setattr(env_loader, "load_lab_env", lambda root: None)
    provider = FakeProvider([ModelResponse(text="Xin chào nhóm NgaMy!")])
    monkeypatch.setattr(providers, "make_provider", lambda name: provider)
    original_save = ui.save_session
    monkeypatch.setattr(ui, "save_session", lambda s: original_save(s, tmp_path))
    app = AppTest.from_file(str(ui.ROOT / "app.py"), default_timeout=20).run()
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Trò chuyện", "Công cụ & cấu hình", "Phiên bản Agent", "Lịch sử chat",
    ]
    assert any("position: fixed" in element.value for element in app.markdown)
    assert any(element.value == "Lịch sử phiên chat sẽ được lưu lại ở đây." for element in app.caption)
    app.session_state["research_tabs"] = "Công cụ & cấu hình"
    app.run()
    assert not app.exception
    assert not app.chat_input
    app.session_state["research_tabs"] = "Lịch sử chat"
    app.run()
    assert not app.exception
    assert not app.chat_input
    app.session_state["research_tabs"] = "Trò chuyện"
    app.run()
    assert not app.exception
    assert len(app.chat_input) == 1
    app.chat_input[0].set_value("Xin chào").run()
    assert not app.exception
    assert any("position: fixed" in element.value for element in app.markdown)
    assert len(app.session_state.research["turns"]) == 1
    assert app.session_state.research["turns"][0]["assistant_text"] == "Xin chào nhóm NgaMy!"
    assert app.session_state.research["turns"][0]["version"] == "v4"
    assert app.session_state.research["turns"][0]["artifact_version"] == app.session_state.research["artifact_version"]
    assert any("Agent v4" in caption.value for caption in app.caption)
    assert len(list(tmp_path.glob("*.transcript.json"))) == 1
    old_id = app.session_state.research["transcript_id"]
    next(b for b in app.button if b.label == "Áp dụng version & tạo phiên mới").click().run()
    assert not app.exception
    assert app.session_state.research["turns"] == []
    assert app.session_state.research["transcript_id"] != old_id
    assert any("position: fixed" in element.value for element in app.markdown)


def test_streamlit_version_selection_changes_chat_configuration(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest
    import env_loader
    import providers
    monkeypatch.setattr(env_loader, "load_lab_env", lambda root: None)
    monkeypatch.setattr(providers, "make_provider", lambda name: FakeProvider([]))
    original_save = ui.save_session
    monkeypatch.setattr(ui, "save_session", lambda s: original_save(s, tmp_path))

    app = AppTest.from_file(str(ui.ROOT / "app.py"), default_timeout=20).run()
    assert not app.exception
    assert app.session_state.research["version"] == "v4"
    next(s for s in app.selectbox if s.label == "Version agent").select("v2").run()
    assert not app.exception
    assert any("v2" in element.value for element in app.code)
    next(b for b in app.button if b.label == "Áp dụng version & tạo phiên mới").click().run()
    assert not app.exception
    assert app.session_state.research["version"] == "v2"
    assert len(app.session_state.research["declarations_snapshot"]) == 10
    assert app.session_state.research["artifact_version"] == "v2+pea21801f0290+t64a6349a4b00"
