import numpy as np
import pytest

import dash_io as dio

array = np.array([[1, 2, 3], [4, 5, 6]])


def test_array():
    encoded = dio.url_from_numpy(array)
    decoded = dio.url_to_numpy(encoded)

    np.testing.assert_array_equal(array, decoded)


def test_allow_pickle():
    with pytest.raises(ValueError):
        encoded = dio.url_from_numpy(array, allow_pickle=False)
        encoded = dio.url_from_numpy(array, allow_pickle=True)

    with pytest.raises(ValueError):
        encoded = dio.url_from_numpy(array)
        decoded = dio.url_to_numpy(encoded, allow_pickle=False)
        decoded = dio.url_to_numpy(encoded, allow_pickle=True)
