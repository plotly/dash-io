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
data_url = dim.encode_pillow(im)

# Decode the data url into a PIL image
im = dim.decode_pillow(data_url)
```

The following format are currently supported: `jpg`, `png`

### Pandas

The following format are currently supported: `jpg`, `png`

```python
import pandas as pd
import dash_io.mime as dim

data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
df = pd.read_csv(data)

encoded = dim.encode_pandas(df, format="csv", mime_type="text", mime_subtype="csv", index=False)
decoded = dim.decode_pandas(encoded, format="csv")
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
pip install -e .[dev]
```

Run pytest:
```
python -m pytest
```