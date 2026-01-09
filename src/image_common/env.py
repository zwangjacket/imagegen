"""Environment helpers shared across components."""

from __future__ import annotations

import os


def save_clean_copy_enabled() -> bool:
    value = os.getenv("SAVE_CLEAN_COPY", "")
    if not value.strip():
        return False
    return as_boolean(value, key="SAVE_CLEAN_COPY")


def as_boolean(value: str, *, key: str | None = None) -> bool:
    if not key:
        key = "key"
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(
        f"value {value} for {key} must be one of 1, 0, true, false, yes, no, on, off"
    )
