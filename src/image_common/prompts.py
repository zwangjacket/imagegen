"""Prompt helpers shared across components."""

from __future__ import annotations

from pathlib import Path


def list_prompt_names(prompts_dir: Path) -> list[str]:
    names: list[str] = []
    for path in prompts_dir.glob("*.txt"):
        names.append(path.stem)
    return sorted(names)


def prompt_path(prompts_dir: Path, prompt_name: str) -> Path:
    sanitized = normalize_prompt_name(prompt_name)
    return prompts_dir / f"{sanitized}.txt"


def normalize_prompt_name(raw_name: str) -> str:
    candidate = raw_name.strip()
    if not candidate:
        return ""
    candidate = Path(candidate).name
    if candidate.endswith(".txt"):
        candidate = candidate[:-4]
    return candidate


def write_prompt(path: Path, text: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_text(normalized, encoding="utf-8")


def read_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_multivalue_field(raw_value: str) -> list[str]:
    values: list[str] = []
    for chunk in raw_value.splitlines():
        parts = [part.strip() for part in chunk.split(",") if part.strip()]
        values.extend(parts)
    return values
