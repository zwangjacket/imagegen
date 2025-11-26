from __future__ import annotations

from pathlib import Path

import pytest

import imagegen.options as options_module


@pytest.fixture()
def test_env_file(tmp_path, monkeypatch) -> Path:
    """Provide an isolated .env file for each test that needs CLI parsing."""

    env_path = tmp_path / ".env"
    env_path.write_text(
        "\n".join(
            [
                "FAL_KEY=test-key",
                "SAFETENSORS_URL=https://example.com/j/",
                "SOURCE_IMAGE_URL=https://example.com/k/",
            ]
        )
    )
    monkeypatch.setattr(options_module, "_DOTENV_FILE", env_path)
    return env_path
