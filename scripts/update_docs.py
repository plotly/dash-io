import pydoc

import dash_io as dio


generated = pydoc.render_doc(dio, renderer=pydoc.plaintext)
generated = generated.split("\nFILE\n")[0].strip()

with open("DOCS.txt", "w") as f:
    f.write(generated)
