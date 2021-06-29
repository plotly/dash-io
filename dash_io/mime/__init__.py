import base64
import os
import json
from io import BytesIO, StringIO
import pickle

import pandas as pd
from PIL import Image


# Helper functions
def _infer_buffer(mime_type, mime_subtype):
    if mime_type == "application" and mime_subtype == "octet-stream":
        return BytesIO()
    elif mime_type == "text" and mime_subtype == "csv":
        return StringIO()
    else:
        error_msg = "Incorrect type or subtype. Please choose mime_type='application' and mime_subtype='octet-stream', or mime_type='text' and mime_subtype='csv'."
        raise ValueError(error_msg)


def _validate_data_prefix(data_url):
    if data_url.startswith("data:"):
        data_url = data_url[5:]
        return data_url
    else:
        error_msg = f'The data_url "{data_url[:30]}..." is invalid. It should start with "data:".'
        raise ValueError(error_msg)


def _validate_b64_header(header):
    if header.endswith(";base64"):
        mediatype = header[:-7]
        return mediatype
    else:
        error_msg = f'The header "{header}..." is invalid. It should end with "base64".'
        raise ValueError(error_msg)


def _validate_format(format, accepted):
    format = format.lower()
    if format not in accepted:
        error_msg = f'Format "{format}" cannot be encoded. Please choose an accepted format: {accepted}'
        raise ValueError(error_msg)

    return format


# Main functions


def get_format(filename):
    parts = os.path.splitext(filename)
    extension = parts[-1][1:]
    return extension


def encode_pillow(im, format="png", mime_type="image", mime_subtype=None, **kwargs):
    format = _validate_format(format, accepted=("png", "jpg", "jpeg", "gif"))

    # comply to mime types
    if format == "jpg":
        format = "jpeg"

    # If no mime subtype is given, we infer from format
    mime_subtype = format if mime_subtype is None else mime_subtype

    # If the image has transparency and we want to save it as JPEG, need to remove the
    # last dimension A.
    if format == "jpeg" and im.mode in ("RGBA", "LA"):
        background = Image.new(im.mode[:-1], im.size, (255, 255, 255))
        background.paste(im, im.split()[-1])
        im = background

    buffer = BytesIO()
    im.save(buffer, format=format, **kwargs)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:{mime_type}/{mime_subtype};base64,{encoded}"


def decode_pillow(data_url, accepted=("png", "jpeg"), **kwargs):
    data_url = _validate_data_prefix(data_url)
    header, data = data_url.split(",")
    mime_type, mime_subtype = _validate_b64_header(header).split("/")

    decoded = base64.b64decode(data)
    buffer = BytesIO(decoded)

    
    print(mime_subtype.upper())

    Image.init()
    print("Image ID:", Image.ID)

    if accepted == "all":
        im = Image.open(buffer, **kwargs)

    elif mime_subtype in accepted:
        kwargs['formats'] = [mime_subtype.upper()]
        im = Image.open(buffer, **kwargs)
    
    else:
        error_msg = (
            f'"{mime_type}" is not a format accepted {accepted}. Please choose a format that is accepted, '
            'add your desired format to the accepted tuple, or set accepted="all" if you want to bypass '
            "the security check (only do this if the file you are decoding is trusted)."
        )
        raise ValueError(error_msg)
    
    return im


def encode_pandas(
    df, format="csv", mime_type="application", mime_subtype="octet-stream", **kwargs
):
    format = _validate_format(format, accepted=("csv", "parquet", "pickle", "xlsx"))

    buffer = _infer_buffer(mime_type, mime_subtype)

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
    format = _validate_format(format, accepted=("csv", "parquet", "pickle", "xlsx"))

    data_url = _validate_data_prefix(data_url)
    header, data = data_url.split(",")
    mime_type, mime_subtype = _validate_b64_header(header).split("/")

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


def encode_json(obj, mime_type="application", mime_subtype="json", **kwargs):
    dumped = json.dumps(obj, **kwargs).encode("utf-8")
    encoded = base64.b64encode(dumped).decode("utf-8")
    return f"data:{mime_type}/{mime_subtype};base64,{encoded}"


def decode_json(data_url, **kwargs):
    data_url = _validate_data_prefix(data_url)
    header, data = data_url.split(",")
    _validate_b64_header(header)

    decoded = base64.b64decode(data)

    return json.loads(decoded, **kwargs)
