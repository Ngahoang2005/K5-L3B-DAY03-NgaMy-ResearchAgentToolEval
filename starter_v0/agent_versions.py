"""Historical agent configurations available in the Streamlit UI."""
from __future__ import annotations

from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
VERSION_ARTIFACTS = ARTIFACTS / "agent_versions"
SHARED_PROMPT = VERSION_ARTIFACTS / "shared" / "system_prompt.md"


@dataclass(frozen=True)
class AgentVersion:
    version: str
    title: str
    prompt_path: Path
    tools_path: Path
    prompt_hash: str
    tools_hash: str
    accuracy: str
    changes: tuple[str, ...]
    source: str


AGENT_VERSIONS = {
    "v0": AgentVersion(
        version="v0",
        title="Baseline",
        prompt_path=ARTIFACTS / "agent_versions" / "v0" / "system_prompt.md",
        tools_path=ARTIFACTS / "agent_versions" / "v0" / "tools.yaml",
        prompt_hash="eb1c8179815b",
        tools_hash="e69bc53ed884",
        accuracy="0.70",
        changes=("Bản nền ban đầu, trước khi cải thiện prompt và tool declaration.",),
        source="Khôi phục từ starter trong Git (ff7427d); snapshot không trùng fingerprint run v0.",
    ),
    "v1": AgentVersion(
        version="v1",
        title="Cải thiện system prompt",
        prompt_path=SHARED_PROMPT,
        tools_path=VERSION_ARTIFACTS / "v1" / "tools.yaml",
        prompt_hash="ea21801f0290",
        tools_hash="e69bc53ed884",
        accuracy="0.95",
        changes=(
            "Hỏi lại khi thiếu thông tin thay vì đoán.",
            "Yêu cầu xác nhận rõ trước khi gửi/đăng.",
            "Cho phép trả lời ngoài phạm vi nghiên cứu trực tiếp và phối hợp nhiều tool.",
        ),
        source="Prompt khớp fingerprint v1; declaration baseline lưu trong repo, fingerprint run không khớp.",
    ),
    "v2": AgentVersion(
        version="v2",
        title="Viết lại tool declaration",
        prompt_path=SHARED_PROMPT,
        tools_path=VERSION_ARTIFACTS / "v2" / "tools.yaml",
        prompt_hash="ea21801f0290",
        tools_hash="64a6349a4b00",
        accuracy="1.00",
        changes=(
            "Nêu rõ khi nào dùng và không dùng từng tool.",
            "Chuẩn hóa query, topic/timeframe và tham số.",
            "Ưu tiên clarify dạng yes/no trước yêu cầu gửi/đăng.",
        ),
        source="Snapshot prompt và tools khớp fingerprint đã ghi cho v2.",
    ),
    "v3": AgentVersion(
        version="v3",
        title="Cải thiện định tuyến policy_area",
        prompt_path=SHARED_PROMPT,
        tools_path=VERSION_ARTIFACTS / "v3" / "tools.yaml",
        prompt_hash="ea21801f0290",
        tools_hash="544c396ba964",
        accuracy="0.95 / 1.00 (hai lần chạy base)",
        changes=(
            "Làm rõ cách chọn policy_area theo loại câu hỏi.",
            "Chỉ chọn all khi câu hỏi thực sự bao quát nhiều vùng.",
            "Độ chính xác base dao động giữa hai lần chạy; extension đạt 1.00.",
        ),
        source="Snapshot từ commit v3 gần nhất (16cec98); fingerprint run không khớp.",
    ),
    "v4": AgentVersion(
        version="v4",
        title="Bổ sung bốn tool nghiên cứu",
        prompt_path=SHARED_PROMPT,
        tools_path=VERSION_ARTIFACTS / "v4" / "tools.yaml",
        prompt_hash="ea21801f0290",
        tools_hash="85fc98b68764",
        accuracy="1.00 base / 1.00 group",
        changes=(
            "Thêm wiki để tra cứu bối cảnh Wikipedia.",
            "Thêm hn để tìm thảo luận Hacker News.",
            "Thêm github để tìm repository và hf để tìm model trên Hugging Face.",
        ),
        source="Snapshot v4 hiện tại; fingerprint prompt và tools khớp run v4.",
    ),
}


def version_diff(version: str) -> str:
    versions = list(AGENT_VERSIONS)
    if version not in AGENT_VERSIONS:
        raise ValueError(f"Version agent không tồn tại: {version}")
    index = versions.index(version)
    if index == 0:
        return "v0 là baseline, chưa có version trước để so sánh."

    previous = AGENT_VERSIONS[versions[index - 1]]
    current = AGENT_VERSIONS[version]
    sections = []
    for label, old_path, new_path in (
        ("System prompt", previous.prompt_path, current.prompt_path),
        ("Tool declaration", previous.tools_path, current.tools_path),
    ):
        diff = list(unified_diff(
            old_path.read_text(encoding="utf-8").splitlines(),
            new_path.read_text(encoding="utf-8").splitlines(),
            fromfile=f"{previous.version}/{label}",
            tofile=f"{current.version}/{label}",
            lineterm="",
            n=2,
        ))
        if diff:
            sections.extend(diff)
    return "\n".join(sections) if sections else "Không có thay đổi nội dung so với version trước."
