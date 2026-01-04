from __future__ import annotations

import random
from datetime import datetime

import piexif
from PIL import Image

from imagegen import exif


def test_set_exif_data_rewrites_exif_and_description(tmp_path):
    image_path = tmp_path / "sample.jpg"
    Image.new("RGB", (32, 32), color="white").save(image_path)

    fixed_time = datetime(2024, 1, 2, 3, 4, 5)
    deterministic_rng = random.Random(42)  # noqa: S311

    assert exif.set_exif_data(
        image_path,
        description="enchanted forest",
        rng=deterministic_rng,
        file_time=fixed_time,
    )

    metadata = piexif.load(str(image_path))
    assert metadata["0th"][piexif.ImageIFD.ImageDescription] == b"enchanted forest"
    assert metadata["0th"][piexif.ImageIFD.Make] == exif.DEFAULT_CAMERA_MAKE.encode()

    # Running again without a description should fully rewrite EXIF and omit the tag
    assert exif.set_exif_data(
        image_path,
        rng=deterministic_rng,
        file_time=fixed_time,
    )
    metadata = piexif.load(str(image_path))
    assert piexif.ImageIFD.ImageDescription not in metadata["0th"]
