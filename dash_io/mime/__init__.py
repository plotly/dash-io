import base64
from io import BytesIO, StringIO

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


def _verify_format(format, accepted):
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
    format = _verify_format(format, accepted=("png", "jpg", "jpeg"))

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
    header, data = data_url.split(",")
    _verify_b64_header(header)

    decoded = base64.b64decode(data)
    buffer = BytesIO(decoded)
    im = Image.open(buffer)

    return im


def encode_pandas(
    df, format="csv", mime_type="application", mime_subtype="octet-stream", **kwargs
):
    format = _verify_format(format, accepted=("csv", "parquet", "pickle", "xlsx"))

    if mime_type == "application" and mime_subtype == "octet-stream":
        buffer = BytesIO()
    elif mime_type == "text" and mime_subtype == "csv":
        buffer = StringIO()
    else:
        error_msg = "Incorrect type or subtype. Please choose mime_type='application' and mime_subtype='octet-stream', or mime_type='text' and mime_subtype='csv'."
        raise ValueError(error_msg)

    if format == "csv":
        df.to_csv(buffer, **kwargs)
    elif format == "parquet":
        df.to_parquet(buffer, **kwargs)
    elif format == "pickle":
        df.to_pickle(buffer, **kwargs)
    elif format == "xlsx":
        df.to_excel(buffer, **kwargs)

    buffer_val = buffer.getvalue()

    if mime_type == "text" and mime_subtype == "csv":
        buffer_val = buffer_val.encode("utf-8")

    encoded = base64.b64encode(buffer_val).decode("utf-8")

    return f"data:{mime_type}/{mime_subtype};base64,{encoded}"


def decode_pandas(data_url, format="csv", **kwargs):
    format = _verify_format(format, accepted=("csv", "parquet", "pickle", "xlsx"))

    data_url = _verify_data_prefix(data_url)
    header, data = data_url.split(",")
    mime_type, mime_subtype = _verify_b64_header(header).split("/")
    decoded = base64.b64decode(data)

    if mime_type == "text" and mime_subtype == "csv":
        buffer = StringIO(decoded.decode("utf-8"))
    elif mime_type == "application" and mime_subtype == "octet-stream":
        buffer = BytesIO(decoded)
    else:
        error_msg = "Incorrect type or subtype. Please make sure the MIME type (aka media type) is 'text/csv' for CSV or 'application/octet-stream' for binary encoded."
        raise ValueError(error_msg)

    if format == "csv":
        df = pd.read_csv(buffer, **kwargs)
    elif format == "parquet":
        df = pd.read_parquet(buffer, **kwargs)
    elif format == "pickle":
        df = pd.read_pickle(buffer, **kwargs)
    elif format == "xlsx":
        df = pd.read_excel(buffer, **kwargs)

    return df
