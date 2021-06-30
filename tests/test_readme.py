import pydoc

import dash_io as dio


def test_readme():
    generated = pydoc.render_doc(dio, renderer=pydoc.plaintext)
    generated = generated.split("\nFILE\n")[0].strip()

    with open("README.md", "r") as f:
        assert generated in f.read()
