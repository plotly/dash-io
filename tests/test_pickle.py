import dash_io.mime as dim


class ExampleClass:
    num = 35
    st = "hey"

    def __eq__(self, other):
        return (self.num == other.num) and (self.st == other.st)


def test_list_of_dicts():
    ls = [{"one": 1}, 2, 3, {"foo": True}, "日本"]
    encoded = dim.encode_pickle(ls)
    decoded = dim.decode_pickle(encoded)

    assert ls == decoded


def test_nested_dict():
    di = {"two": 2, "foo": "bar", "日本": True, "numbers": [5, 0, 2, 1]}
    encoded = dim.encode_pickle(di)
    decoded = dim.decode_pickle(encoded)

    assert di == decoded


def test_object():
    obj = ExampleClass()

    encoded = dim.encode_pickle(obj)
    decoded = dim.decode_pickle(encoded)

    assert obj == decoded
