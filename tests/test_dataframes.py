import pandas as pd

import dash_io.mime as dim

assert_fail_msg = "Original dataframe does not match decoded dataframe."


df = pd.read_csv("tests/data/sample.csv")


def test_csv_stringio():
    encoded = dim.encode_pandas(
        df, format="csv", mime_type="text", mime_subtype="csv", index=False
    )
    decoded = dim.decode_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)


def test_csv_bytesio():
    encoded = dim.encode_pandas(df, format="csv", index=False)
    decoded = dim.decode_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)


def test_xlsx():
    encoded = dim.encode_pandas(df, format="xlsx", index=False)
    decoded = dim.decode_pandas(encoded, format="xlsx")

    pd.testing.assert_frame_equal(df, decoded)


def test_xls():
    encoded = dim.encode_pandas(df, format="xls", index=False)
    decoded = dim.decode_pandas(encoded, format="xls")

    pd.testing.assert_frame_equal(df, decoded)


def test_parquet():
    encoded = dim.encode_pandas(df, format="parquet")
    decoded = dim.decode_pandas(encoded, format="parquet")

    pd.testing.assert_frame_equal(df, decoded)


def test_pickle():
    encoded = dim.encode_pandas(df, format="pickle")
    decoded = dim.decode_pandas(encoded, format="pickle")

    pd.testing.assert_frame_equal(df, decoded)
