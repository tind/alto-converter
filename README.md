# Alto parser and converter

This Python package is an experimental Alto parser and converter. It
parses the Alto file using SAX into a datastructure, then this
datastructure can be used to produce other formats. HOCR conversion is
bundled, see `app.py` for an example usage.

# Requirements

You need at least Python 2.7, should work fine with Python 3 as
well. For HOCR conversion you need Jinja.
