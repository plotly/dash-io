import sys

import pandas as pd
import pytest

import dash_io as dio

assert_fail_msg = "Original dataframe does not match decoded dataframe."


df = pd.read_csv("tests/data/sample.csv")


def test_csv_stringio():
    # Test implicitly
    encoded = dio.url_from_pandas(df, format="csv", index=False)
    decoded = dio.url_to_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)

    # Test explicitly
    encoded = dio.url_from_pandas(
        df, format="csv", mime_type="text", mime_subtype="csv", index=False
    )
    decoded = dio.url_to_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)


@pytest.mark.skipif(
    pd.__version__ < '1.2.0',
    reason="Saving CSV to BytesIO is not supported in pandas 1.1",
)
def test_csv_bytesio():
    encoded = dio.url_from_pandas(
        df,
        format="csv",
        mime_type="application",
        mime_subtype="octet-stream",
        index=False,
    )
    decoded = dio.url_to_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)


def test_xlsx():
    encoded = dio.url_from_pandas(df, format="xlsx", index=False)
    decoded = dio.url_to_pandas(encoded, format="xlsx")

    pd.testing.assert_frame_equal(df, decoded)


def test_xls():
    encoded = dio.url_from_pandas(df, format="xls", index=False)
    decoded = dio.url_to_pandas(encoded, format="xls")

    pd.testing.assert_frame_equal(df, decoded)


def test_parquet():
    encoded = dio.url_from_pandas(df, format="parquet")
    decoded = dio.url_to_pandas(encoded, format="parquet")

    pd.testing.assert_frame_equal(df, decoded)


def test_feather():
    encoded = dio.url_from_pandas(df, format="feather")
    decoded = dio.url_to_pandas(encoded, format="feather")

    pd.testing.assert_frame_equal(df, decoded)
