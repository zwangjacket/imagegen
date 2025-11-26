import sys
from pathlib import Path

import pytest

import imagegen.options as options_module
from imagegen import main as imagegen_main

pytestmark = pytest.mark.usefixtures("test_env_file")


def run_main_argv(argv: list[str], capsys):
    # Patch sys.argv and run main, capture stdout
    old_argv = sys.argv
    try:
        sys.argv = ["imagegen"] + argv
        imagegen_main()
        out = capsys.readouterr().out
        return out
    finally:
        sys.argv = old_argv


@pytest.mark.parametrize(
    "argv,expected_paths",
    [
        (["schnell", "-p", "hello"], [Path("assets/schnell-1.png")]),
        (
            ["dev", "-p", "hi", "-#", "2"],
            [Path("assets/dev-1.png"), Path("assets/dev-2.png")],
        ),
    ],
)
def test_main_streams_generated_paths(monkeypatch, argv, expected_paths, capsys):
    """Ensures main() prints the generated image paths, in order, for each model.

    Why: The CLI is used in pipelines; it must stream only the output file paths
    (one per line) so downstream tools can consume them reliably. This also
    verifies dotenv is loaded before generation and that the selected model name
    is passed through to generation logic.
    """
    produced = []

    def fake_generate(parsed, *, output_dir=None):
        produced.append(parsed.model)
        return expected_paths

    def fake_load_dotenv(path):  # noqa: ARG001 - signature matches load_dotenv
        produced.append("dotenv")
        return True

    monkeypatch.setattr(options_module, "load_dotenv", fake_load_dotenv)
    monkeypatch.setitem(sys.modules, "fal_client", type("F", (), {})())
    monkeypatch.setattr(
        "imagegen.imagegen.generate_images", fake_generate, raising=False
    )

    out = run_main_argv(argv, capsys)
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    assert lines == [str(path) for path in expected_paths]
    assert produced[0] == "dotenv"
    assert produced[1] == argv[0]
