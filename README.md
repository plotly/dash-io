# dash-io

An API prototype for simplifying IO in Dash. This is an experimental library and not an official Plotly product.

## Quickstart

To install the library:
```bash
pip install dash-io
```

Start using it inside Python
```python
import dash_io as dio

# ...

url_df = dio.url_from_pandas(df)  # dataframe
url_im = dio.url_from_pillow(im)  # PIL image

# ...

df = dio.url_to_pandas(url_df)
im = dio.url_to_pillow(url_im)
```

## Usage

### Pillow

```python
from PIL import Image
import numpy as np
import dash_io as dio

# Dummy image in Pillow
im = Image.fromarray(np.random.randint(0, 255, (100,100,3)))

# Encode the image into a data url
data_url = dio.url_from_pillow(im, format="jpg")

# Decode the data url into a PIL image
im = dio.url_to_pillow(data_url, format="jpg")
```

The following format are currently supported: `jpg`, `png`.

### Pandas

If you use `xlsx`, make sure to install a third-party engine such as `openpyxl`.

To use it in pandas:
```python
import pandas as pd
import dash_io as dio

# Dummy data
data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
df = pd.DataFrame.from_dict(data)

# To encode/decode in binary CSV format
encoded = dio.url_from_pandas(df, format="csv", index=False)
decoded = dio.url_to_pandas(encoded, format="csv")

# To encode/decode in binary parquet format
encoded = dio.url_from_pandas(df, format="parquet")
decoded = dio.url_to_pandas(encoded, format="parquet")

# To encode/decode in string CSV format (i.e. text/csv MIME type)
encoded = dio.url_from_pandas(df, format="csv", mime_type="text", mime_subtype="csv", index=False)
decoded = dio.url_to_pandas(encoded, format="csv")
```

The following format are currently supported: `csv`, `parquet`, `feather`, `xlsx`.


### JSON

```python
import dash_io as dio

# Encode/decode dictionary
data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
encoded = dio.url_from_json(data)
decoded = dio.url_to_json(encoded)

# It also works with lists and other JSON-serializable objects
encoded = dio.url_from_json([1,2,3,4,5])
```

Note that if a `dict` key is an integer, it will be converted to string by `json`. This is a normal behavior.


## Documentation

You can access the documentation by calling:
```python
import dash_io as dio
help(dio)
```

You can find the up-to-date output from `help` inside [`DOCS.txt`](DOCS.txt).


## Development

First, clone this repo:
```bash
git clone https://github.com/plotly/dash-io
```

### Testing

Create a venv:
```bash
python -m venv venv
source venv/bin/activate
```

Install dev dependencies:
```bash
cd dash-io
pip install requirements-dev.txt
```

Run pytest:
```
python -m pytest
```
