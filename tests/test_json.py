import dash_io.mime as dim


def test_list():
    ls = [1, 2, 3, "foo", True, "日本"]
    encoded = dim.encode_json(ls)
    decoded = dim.decode_json(encoded)

    assert ls == decoded


def test_list_of_dicts():
    ls = [{"one": 1}, 2, 3, {"foo": True}, "日本"]
    encoded = dim.encode_json(ls)
    decoded = dim.decode_json(encoded)

    assert ls == decoded


def test_flat_dict():
    di = {"two": 2, "foo": "bar", "日本": True}
    encoded = dim.encode_json(di)
    decoded = dim.decode_json(encoded)

    assert di == decoded


def test_nested_dict():
    di = {"two": 2, "foo": "bar", "日本": True, "numbers": [5, 0, 2, 1]}
    encoded = dim.encode_json(di)
    decoded = dim.decode_json(encoded)

    assert di == decoded

    di = {"col_1": [3, 2, 1, 0], "col_2": ["a", "b", "c", "d"]}
    encoded = dim.encode_json(di)
    decoded = dim.decode_json(encoded)

    assert di == decoded
