import sys

import pandas as pd
import pytest

import dash_io.mime as dim


def __pandas_is(*versions):
    major, minor, patch = pd.__version__.split(".")
    return ".".join([major, minor]) in versions


assert_fail_msg = "Original dataframe does not match decoded dataframe."


df = pd.read_csv("tests/data/sample.csv")


def test_csv_stringio():
    # Test implicitly
    encoded = dim.encode_pandas(df, format="csv", index=False)
    decoded = dim.decode_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)

    # Test explicitly
    encoded = dim.encode_pandas(
        df, format="csv", mime_type="text", mime_subtype="csv", index=False
    )
    decoded = dim.decode_pandas(encoded, format="csv")

    pd.testing.assert_frame_equal(df, decoded)


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="Saving CSV to BytesIO is not supported in pandas 1.1",
)
def test_csv_bytesio():
    encoded = dim.encode_pandas(
        df,
        format="csv",
        mime_type="application",
        mime_subtype="octet-stream",
        index=False,
    )
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


@pytest.mark.skipif(
    sys.version_info < (3, 7),
    reason="Infer pickle compression is not supported in pandas 1.1 or below",
)
def test_pickle():
    encoded = dim.encode_pandas(df, format="pickle")
    decoded = dim.decode_pandas(encoded, format="pickle")

    pd.testing.assert_frame_equal(df, decoded)


@pytest.mark.skipif(
    __pandas_is("0.25", "1.0", "1.1"),
    reason="Loading/saving pickle to memory v0.25, v1.0, v1.1",
)
def test_pickle_no_compression():
    encoded = dim.encode_pandas(df, format="pickle", compression=None)
    decoded = dim.decode_pandas(encoded, format="pickle", compression=None)

    pd.testing.assert_frame_equal(df, decoded)
