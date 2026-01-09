"""Prompt helpers for imageedit services."""

from __future__ import annotations

import re
from pathlib import Path

from image_common.prompts import normalize_prompt_name, read_prompt


def append_style_prompt(prompt_text: str, styles_dir: Path, style_name: str) -> str:
    sanitized = normalize_prompt_name(style_name)
    if not sanitized:
        return prompt_text

    style_path = styles_dir / f"{sanitized}.txt"
    if not style_path.exists():
        return prompt_text

    style_text = read_prompt(style_path)
    normalized_style = style_text.replace("\r\n", "\n").replace("\r", "\n")
    normalized_prompt = prompt_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized_prompt.splitlines()
    for index, line in enumerate(lines):
        if line.lower().startswith("style:"):
            lines = lines[:index]
            break

    base = "\n".join(lines).rstrip()
    style_line = f"Style: {sanitized}"
    if base and normalized_style:
        return f"{base}\n{style_line}\n{normalized_style}"
    if base:
        return f"{base}\n{style_line}"
    if normalized_style:
        return f"{style_line}\n{normalized_style}"
    return style_line


def next_copy_name(prompt_name: str) -> str:
    match = re.fullmatch(r"(.+)_copy(\d+)?", prompt_name)
    if match:
        base = match.group(1)
        number = match.group(2)
        if number is None:
            return f"{base}_copy2"
        return f"{base}_copy{int(number) + 1}"
    return f"{prompt_name}_copy"
