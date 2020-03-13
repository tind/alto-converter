# Alto parser and converter

This Python package is an experimental Alto parser and converter. It
parses the Alto file using SAX into a datastructure, then this
datastructure can be used to produce other formats. HOCR conversion is
bundled, see `app.py` for an example usage.

# Requirements

You need at least Python 2.7, should work fine with Python 3 as
well. For hOCR conversion you need Jinja.

# Acknowledgements

The `get_box` logic in the Alto parser and large parts of the hOCR template were inspired
by the [`abbyy2hocr.xsl` template](https://github.com/OCR-D/format-converters/blob/9615db1920cb8e15a38427333b41cdbee8baf4b6/abbyy2hocr.xsl),
distributed by OCR-D on GitHub.
