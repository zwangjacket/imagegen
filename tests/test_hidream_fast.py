import pytest

from imagegen.options import build_parser, parse_args
from imagegen.registry import MODEL_REGISTRY

pytestmark = pytest.mark.usefixtures("test_env_file")


def test_hidream_fast_defaults():
    """Ensures hidream-fast exposes documented defaults and auto seed handling."""
    parser = build_parser(MODEL_REGISTRY)
    ns = parse_args(
        ["hidream-fast", "-p", "test sketch"],
        registry=MODEL_REGISTRY,
        parser=parser,
    )

    params = ns.params
    assert ns.model == "hidream-fast"
    assert params["prompt"] == "test sketch"
    assert params["negative_prompt"] == ""
    assert params["image_size"] == "portrait_4_3"
    assert params["num_inference_steps"] == 16
    assert params["num_images"] == 1
    assert params["enable_safety_checker"] is False
    assert params["output_format"] == "jpeg"
    assert isinstance(params["seed"], int) and params["seed"] >= 0


def test_hidream_fast_overrides():
    """Covers flag overrides for hidream-fast specific options."""
    parser = build_parser(MODEL_REGISTRY)
    ns = parse_args(
        [
            "hidream-fast",
            "-p",
            "prompt",
            "-n",
            "blurry, low quality",
            "-i",
            "square_hd",
            "-#",
            "2",
            "-s",
            "123",
            "--enable-safety-checker",
            "--output-format",
            "png",
        ],
        registry=MODEL_REGISTRY,
        parser=parser,
    )

    params = ns.params
    assert params["negative_prompt"] == "blurry, low quality"
    assert params["image_size"] == "square_hd"
    assert params["num_images"] == 2
    assert params["enable_safety_checker"] is True
    assert params["seed"] == 123
    assert params["output_format"] == "png"
