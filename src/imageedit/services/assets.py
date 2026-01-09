"""Asset helpers for imageedit."""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from image_common.prompts import normalize_prompt_name


def build_asset_entries(paths: Sequence[str], assets_dir: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for raw in paths:
        filename = relative_asset_path(Path(raw), assets_dir)
        entries.append({"display": raw, "filename": filename})
    return entries


def build_gallery_entries(
    paths: Sequence[Path], assets_dir: Path
) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in paths:
        filename = relative_asset_path(path, assets_dir)
        entries.append({"display": filename, "filename": filename})
    return entries


def resolve_asset_path(assets_dir: Path, filename: str) -> Path | None:
    if not filename:
        return None
    if not assets_dir.is_absolute():
        assets_dir = (Path.cwd() / assets_dir).resolve()
    candidate = (assets_dir / filename).resolve()
    try:
        candidate.relative_to(assets_dir)
    except ValueError:
        return None
    return candidate


def prompt_name_from_asset_filename(filename: str) -> str:
    name = Path(filename).stem
    match = re.search(r"-\d+", name)
    if match:
        name = name[: match.start()]
    return normalize_prompt_name(name)


def list_asset_paths(assets_dir: Path) -> list[Path]:
    if not assets_dir.is_absolute():
        assets_dir = (Path.cwd() / assets_dir).resolve()
    if not assets_dir.exists():
        return []
    allowed_suffixes = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff"}
    candidates = [
        path
        for path in assets_dir.iterdir()
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in allowed_suffixes
    ]
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)


def relative_asset_path(path: Path, assets_dir: Path) -> str:
    target = path if path.is_absolute() else Path.cwd() / path
    try:
        resolved_target = target.resolve()
    except FileNotFoundError:
        resolved_target = target
    assets_root = assets_dir if assets_dir.is_absolute() else Path.cwd() / assets_dir
    try:
        resolved_assets = assets_root.resolve()
    except FileNotFoundError:
        resolved_assets = assets_root
    try:
        return resolved_target.relative_to(resolved_assets).as_posix()
    except ValueError:
        return resolved_target.name
