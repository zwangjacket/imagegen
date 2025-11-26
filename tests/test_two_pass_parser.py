import pytest

from imagegen.options import build_parser, get_safetensors_url, parse_args
from imagegen.registry import MODEL_REGISTRY

pytestmark = pytest.mark.usefixtures("test_env_file")


def test_disallow_options_not_in_model():
    """Rejects options not declared for a model (two-pass parsing guard).

    Why: Each model exposes only a safe/valid subset of options. Passing an
    unknown/unsupported option must fail fast with argparse to prevent sending
    invalid parameters to the FAL API.
    """
    parser = build_parser(MODEL_REGISTRY)
    # schnell does not support --loras; this should raise a SystemExit from argparse
    with pytest.raises(SystemExit):
        parse_args(
            ["schnell", "-p", "x", "--loras", "abc"],
            registry=MODEL_REGISTRY,
            parser=parser,
        )


def test_allow_options_present_in_model():
    """Accepts model-declared options and normalizes their values.

    Why: When a model supports a parameter (e.g., --loras), the parser must
    accept it and map shorthand values to canonical URLs so downstream API calls
    receive fully-qualified values.
    """
    parser = build_parser(MODEL_REGISTRY)
    # krea-lora supports --loras
    ns = parse_args(
        ["krea-lora", "-p", "x", "--loras", "a,b", "--loras", "c"],
        registry=MODEL_REGISTRY,
        parser=parser,
    )
    base = get_safetensors_url().rstrip("/") + "/"
    assert ns.params["loras"] == [
        {"path": f"{base}a.safetensors", "scale": 1},
        {"path": f"{base}b.safetensors", "scale": 1},
        {"path": f"{base}c.safetensors", "scale": 1},
    ]
