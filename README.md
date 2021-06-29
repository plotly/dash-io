# dash-io

An API prototype for simplifying IO in Dash. This is an experimental library and not an official Plotly product.

## Quickstart

To install the library:
```bash
pip install git+https://github.com/plotly/dash-io
```

Start using it inside Python
```python
import dash_io.mime as dim

# ...

url_df = dim.encode_pandas(df)  # dataframe
url_im = dim.encode_pillow(im)  # PIL image

# ...

df = dim.encode_pandas(url_df)
im = dim.encode_pillow(url_im)
```

## Usage

### Pillow

```python
from PIL import Image
import numpy as np
import dash_io.mime as dim

# Dummy image in Pillow
im = Image.fromarray(np.random.randint(0, 255, (100,100,3)))

# Encode the image into a data url
data_url = dim.encode_pillow(im, format="jpg")

# Decode the data url into a PIL image
im = dim.decode_pillow(data_url, format="jpg")
```

The following format are currently supported: `jpg`, `png`.

### Pandas

If you use `parquet` or `xlsx`, make sure to install the correct engines, i.e. `pyarrow` and `openpyxl` respectively.

To use it in pandas:
```python
import pandas as pd
import dash_io.mime as dim

# Dummy data
data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
df = pd.DataFrame.from_dict(data)

# To encode/decode in binary CSV format
encoded = dim.encode_pandas(df, format="csv", index=False)
decoded = dim.decode_pandas(encoded, format="csv")

# To encode/decode in binary parquet format
encoded = dim.encode_pandas(df, format="parquet")
decoded = dim.decode_pandas(encoded, format="parquet")

# To encode/decode in string CSV format (i.e. text/csv MIME type)
encoded = dim.encode_pandas(df, format="csv", mime_type="text", mime_subtype="csv", index=False)
decoded = dim.decode_pandas(encoded, format="csv")
```

The following format are currently supported: `csv`, `parquet`, `pickle`, `xlsx`.


### JSON

```python
import dash_io.mime as dim

# Encode/decode dictionary
data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
encoded = dim.encode_json(data)
decoded = dim.decode_json(encoded)

# It also works with lists and other JSON-serializable objects
encoded = dim.encode_json([1,2,3,4,5])
```

Note that if a `dict` key is an integer, it will be converted to string by `json`. This is a normal behavior.

### Pickle

You can also use pickle to store objects as strings:
```python
import dash_io.mime as dim

class ExampleClass:
    num = 35
    st = "hey"

    def __eq__(self, other):
        return (self.num == other.num) and (self.st == other.st)

obj = ExampleClass()
encoded = dim.encode_pickle(obj)
decoded = dim.decode_pickle(encoded)
```


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