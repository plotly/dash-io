import base64
import os
from io import BytesIO

import pytest
import numpy as np
from PIL import Image, UnidentifiedImageError
import dash_io as dio

assert_fail_msg = "Original image does not match decoded image."


def test_png():
    im = Image.open("tests/data/sample.png")

    encoded = dio.url_from_pillow(im, format="png")
    decoded = dio.url_to_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg


def test_jpg():
    im = Image.open("tests/data/sample.jpg")

    encoded = dio.url_from_pillow(im, format="jpg")
    decoded = dio.url_to_pillow(encoded)

    match_percent = np.mean(np.array(decoded) == np.array(im))

    assert match_percent > 0.964, assert_fail_msg


def test_rgba():
    im = Image.open("tests/data/sample-rgba.png")

    encoded = dio.url_from_pillow(im, format="png")
    decoded = dio.url_to_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg


def test_la():
    im = Image.open("tests/data/sample-la.png")

    encoded = dio.url_from_pillow(im, format="png")
    decoded = dio.url_to_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg


def test_exploit_file():
    # First, open the exploit file (fake png that will run malware)
    file = "tests/data/exploit_image_do_not_open.png"
    with open(file, "rb") as f:
        buffer = BytesIO(f.read())
    # encode the exploit script to base64
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    encoded = f"data:image/png;base64,{encoded}"

    # now, try to decode the exploit script - this should give an error
    with pytest.raises(UnidentifiedImageError):
        dio.url_to_pillow(encoded)
