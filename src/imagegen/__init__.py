"""imagegen package entrypoint.

Currently, main() parses command-line options using imagegen.options
and triggers image generation via imagegen.imagegen.
"""

from __future__ import annotations

import sys

from .options import parse_args


def main() -> None:
    """CLI entrypoint: parse argv, run inference, and persist image assets."""

    parsed = parse_args(sys.argv[1:])

    try:
        from . import imagegen as imagegen_module

        generated_paths = imagegen_module.generate_images(parsed)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    for path in generated_paths:
        print(str(path))
