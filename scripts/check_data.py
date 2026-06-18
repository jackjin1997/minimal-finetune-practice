#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_FILES = ["train.jsonl", "valid.jsonl", "test.jsonl"]
REQUIRED_ROLES = ["system", "user", "assistant"]
REQUIRED_KEYS = ["title", "type", "priority", "due", "owner", "labels", "brief"]
ALLOWED_TYPES = ["bug", "feature", "ops", "research", "docs"]
ALLOWED_PRIORITIES = ["low", "medium", "high", "urgent"]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_file(path: Path, expected_system: str) -> int:
    if not path.exists():
        fail(f"missing {path}")

    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"{path}:{line_no} invalid JSON: {exc}")

            messages = item.get("messages")
            if not isinstance(messages, list) or len(messages) != 3:
                fail(f"{path}:{line_no} expected exactly 3 messages")

            roles = [message.get("role") for message in messages]
            if roles != REQUIRED_ROLES:
                fail(f"{path}:{line_no} expected roles {REQUIRED_ROLES}, got {roles}")

            if messages[0]["content"] != expected_system:
                fail(f"{path}:{line_no} system prompt differs from prompts/system.txt")

            for index, message in enumerate(messages):
                content = message.get("content")
                if not isinstance(content, str) or not content.strip():
                    fail(f"{path}:{line_no} message {index} has empty content")

            try:
                payload = json.loads(messages[-1]["content"])
            except json.JSONDecodeError as exc:
                fail(f"{path}:{line_no} assistant content is not JSON: {exc}")

            if not isinstance(payload, dict):
                fail(f"{path}:{line_no} assistant JSON must be an object")

            keys = list(payload.keys())
            if keys != REQUIRED_KEYS:
                fail(f"{path}:{line_no} expected keys {REQUIRED_KEYS}, got {keys}")

            if not isinstance(payload["title"], str) or not payload["title"].strip():
                fail(f"{path}:{line_no} title must be a non-empty string")

            if payload["type"] not in ALLOWED_TYPES:
                fail(f"{path}:{line_no} invalid type {payload['type']}")

            if payload["priority"] not in ALLOWED_PRIORITIES:
                fail(f"{path}:{line_no} invalid priority {payload['priority']}")

            due = payload["due"]
            if due is not None and (not isinstance(due, str) or not is_valid_date(due)):
                fail(f"{path}:{line_no} due must be YYYY-MM-DD or null")

            owner = payload["owner"]
            if owner is not None and (not isinstance(owner, str) or not owner.strip()):
                fail(f"{path}:{line_no} owner must be a non-empty string or null")

            if not isinstance(payload["labels"], list):
                fail(f"{path}:{line_no} labels must be a list")

            if not all(isinstance(label, str) and label.strip() for label in payload["labels"]):
                fail(f"{path}:{line_no} labels must contain only non-empty strings")

            if not isinstance(payload["brief"], str) or not payload["brief"].strip():
                fail(f"{path}:{line_no} brief must be a non-empty string")

    if count == 0:
        fail(f"{path} has no samples")

    return count


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: check_data.py <data_dir>")

    data_dir = Path(sys.argv[1])
    prompt_path = data_dir.parent / "prompts" / "system.txt"
    if not prompt_path.exists():
        fail(f"missing {prompt_path}")
    expected_system = prompt_path.read_text(encoding="utf-8").strip()

    total = 0
    for name in REQUIRED_FILES:
        count = validate_file(data_dir / name, expected_system)
        total += count
        print(f"{name}: {count} samples")
    print(f"OK: {total} samples")


if __name__ == "__main__":
    main()
