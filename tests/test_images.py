import numpy as np
from PIL import Image
import dash_io.mime as dim

assert_fail_msg = "Original image does not match decoded image."


def test_png():
    im = Image.open("tests/data/sample.png")

    encoded = dim.encode_pillow(im, format="png")
    decoded = dim.decode_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg


def test_jpg():
    im = Image.open("tests/data/sample.jpg")

    encoded = dim.encode_pillow(im, format="jpg")
    decoded = dim.decode_pillow(encoded)

    match_percent = np.mean(np.array(decoded) == np.array(im))

    assert match_percent > 0.964, assert_fail_msg


def test_rgba():
    im = Image.open("tests/data/sample-rgba.png")

    encoded = dim.encode_pillow(im, format="png")
    decoded = dim.decode_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg


def test_la():
    im = Image.open("tests/data/sample-la.png")

    encoded = dim.encode_pillow(im, format="png")
    decoded = dim.decode_pillow(encoded)

    assert np.all(np.array(decoded) == np.array(im)), assert_fail_msg
