# dash-io

An API prototype for simplifying IO in Dash. This is an experimental library and not an official Plotly product.

## Quickstart

To install the library:
```bash
pip install git+https://github.com/plotly/dash-io
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

If you use `parquet` or `xlsx`, make sure to install the correct engines, i.e. `pyarrow` and `openpyxl` respectively.

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

The following format are currently supported: `csv`, `parquet`, `pickle`, `xlsx`.


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

### Pickle

You can also use pickle to store objects as strings:
```python
import dash_io as dio

class ExampleClass:
    num = 35
    st = "hey"

    def __eq__(self, other):
        return (self.num == other.num) and (self.st == other.st)

obj = ExampleClass()
encoded = dio.url_from_pickle(obj)
decoded = dio.url_to_pickle(encoded)
```

#### Note

If you are using Python 3.6, you will need to downgrade `pandas` to `0.24`, since pandas v0.25, v1.0 and v1.1 do not support in-memory pickle loading/saving. Once `pandas==0.24.*`, you will need to set compression to `None`:
```python
encoded = dio.url_from_pickle(obj, compression=None)
decoded = dio.url_to_pickle(encoded, compression=None)
```

## Documentation

You can access the documentation by calling:
```python
import dash_io as dio
help(dio)
```

Here's a (potentially outdated) output of the call above:
```
FUNCTIONS
    get_format(filename)
        Parameters:
            filename (string, required): The name of your file, e.g. "my-image.png" or "my-data.csv"
        
        Returns (string):
            The format of your data, e.g. "png" or "csv"
    
    url_from_json(obj, mime_type='application', mime_subtype='json', **kwargs)
        Parameters:
            obj (object, required): A python object that is JSON-serializable (e.g. a dict, list, string)
            mime_type (string, default="application"): The MIME type to use inside the header: "data:{mime_type}/{mime_subtype};base64,"
            mime_subtype (string, default="json"): The MIME subtype to use inside the header: "data:{mime_type}/{mime_subtype};base64,"
            **kwargs: Arguments passed to the json.dumps
        
        Returns (string):
            A base64-encoded data URL that you can easily send through the web
    
    url_from_pandas(df, format='csv', mime_type=None, mime_subtype=None, **kwargs)
        Parameters:
            df (pd.DataFrame, required): A pandas dataframe that will be converted to a data URL
            format (string, default="csv"): The format to which you want to save your dataframe. Must be one of: "csv", "parquet", "pickle", "xlsx", "xls"
            mime_type (string, default=None): The MIME type to use inside the header: "data:{mime_type}/{mime_subtype};base64,". By default, it will be inferred: "text" if format="csv", "application" otherwise
            mime_subtype (string, default=None): The MIME subtype to use inside the header: "data:{mime_type}/{mime_subtype};base64,". By default, it will be inferred: "csv" if format="csv", "octet-stream" otherwise
            **kwargs: Arguments passed to the pd.read_* function
        
        Returns (string):
            A base64-encoded data URL that you can easily send through the web
    
    url_from_pillow(im, format='png', mime_type='image', mime_subtype=None, **kwargs)
        Parameters:
            im (PIL.Image.Image, required): A Pillow image object that will be converted to a data URL
            format (string, default="png"): The extension of the image. Must be one of "png", "jpg", "jpeg", "gif"
            mime_type (string, default="image"): The MIME type to use inside the header: "data:{mime_type}/{mime_subtype};base64,"
            mime_subtype (string, default=None): The MIME subtype to use inside the header: "data:{mime_type}/{mime_subtype};base64,". By default, it will be inferred from "format"
            **kwargs: Arguments passed to im.save
        
        Returns (string):
            A base64-encoded data URL that you can easily send through the web.
    
    url_to_json(data_url, **kwargs)
        Parameters:
            data_url (string, required): A string that contains the base64-encoded content along with a MIME type header (starts with "data:")
            **kwargs: Arguments passed to the json.loads function
        
        Returns (object):
            A python object was serialized through JSON (e.g. a dict, list, string)
    
    url_to_pandas(data_url, format='csv', **kwargs)
        Parameters:
            data_url (string, required): A string that contains the base64-encoded content along with a MIME type header (starts with "data:")
            format (string, default="csv"): The format in which the file was originally saved by pandas. Must be one of: "csv", "parquet", "pickle", "xlsx", "xls"
            **kwargs: Arguments passed to the pd.read_* function
        
        Returns (pd.DataFrame):
            The pandas dataframe representing your file
    
    url_to_pillow(data_url, accepted=('png', 'jpeg'), **kwargs)
        Parameters:
            data_url (string, required): A string that contains the base64-encoded content along with a MIME type header (starts with "data:")
            accepted (tuple, default=("png", "jpeg")): 
            **kwargs: Arguments passed to the pd.read_* function.
        
        Returns (PIL.Image.Image):
            A Pillow Image object representing your image
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