"""Upload helpers for imageedit."""

from __future__ import annotations

import tempfile
from pathlib import Path

from imagegen.imagegen import upload_image


def upload_local_image(file) -> str:
    if not file:
        raise ValueError("No file provided")
    if not file.filename:
        raise ValueError("No file selected")

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=Path(file.filename).suffix
    ) as temp:
        temp_path = Path(temp.name)
        file.save(temp_path)
        try:
            return upload_image(temp_path)
        finally:
            temp_path.unlink()
