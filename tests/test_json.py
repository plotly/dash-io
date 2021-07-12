import dash_io as dio


def test_list():
    ls = [1, 2, 3, "foo", True, "日本"]
    encoded = dio.url_from_json(ls)
    decoded = dio.url_to_json(encoded)

    assert ls == decoded


def test_list_of_dicts():
    ls = [{"one": 1}, 2, 3, {"foo": True}, "日本"]
    encoded = dio.url_from_json(ls)
    decoded = dio.url_to_json(encoded)

    assert ls == decoded


def test_flat_dict():
    di = {"two": 2, "foo": "bar", "日本": True}
    encoded = dio.url_from_json(di)
    decoded = dio.url_to_json(encoded)

    assert di == decoded


def test_nested_dict():
    di = {"two": 2, "foo": "bar", "日本": True, "numbers": [5, 0, 2, 1]}
    encoded = dio.url_from_json(di)
    decoded = dio.url_to_json(encoded)

    assert di == decoded

    di = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
    encoded = dio.url_from_json(di)
    decoded = dio.url_to_json(encoded)

    assert di == decoded
