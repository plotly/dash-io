import base64
from io import BytesIO

import pandas as pd
from PIL import Image


# Helper functions

def _verify_data_prefix(data_url):
    if data_url.startswith("data:"):
        return data_url[5:]
    else:
        error_msg = f'The data_url "{data_url[:30]}..." is invalid. It should start with "data:".'
        raise ValueError(error_msg)


def _verify_b64_header(header):
    if header.endswith(";base64"):
        mediatype = header[:-7]
        return mediatype
    else:
        error_msg = f'The header "{header}..." is invalid. It should end with "base64".'
        raise ValueError(error_msg)


def _verify_image_format(format, accepted):
    format = format.lower()
    if format not in accepted:
        error_msg = f'Format "{format}" cannot be encoded. Please choose an accepted format: {accepted}'
        raise ValueError(error_msg)

    return format

# Main functions


def get_format(filename):
    parts = filename.split(".")
    extension = parts[-1]
    return extension


def encode_pillow(im, format="png"):
    format = _verify_image_format(format, accepted=('png', 'jpg', 'jpeg'))

    # comply to mime types
    if format == "jpg":
        format = "jpeg"

    if format == "jpeg" and im.mode in ("RGBA", "LA"):
        background = Image.new(im.mode[:-1], im.size, (255, 255, 255))
        background.paste(im, im.split()[-1])
        im = background

    buffer = BytesIO()
    im.save(buffer, format=format)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/{format};base64,{encoded}"


def decode_pillow(data_url):
    data_url = _verify_data_prefix(data_url)
    header, data = data_url.split(',')
    mediatype = _verify_b64_header(header)

    decoded = base64.b64decode(data)
    buffer = BytesIO(decoded)
    im = Image.open(buffer)

    return im
