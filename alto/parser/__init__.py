from xml.sax.handler import ContentHandler

ID = -1
def generate_id():
    ID += 1
    return ID

class HandlerBase(ContentHandler):
    def __init__(self, parser, parent=None, stop_name=""):
        self._parser = parser
        self._parent = parent
        self._stop_name = stop_name
        self._text = []

        self.attrs = dict()

    @classmethod
    def as_sub_handler(cls, parser, parent, name):
        s = cls(parser, parent, name)
        parser.setContentHandler(s)

        return s

    def startElement(self, name, attrs):
        self._text = []

    def endElement(self, name):
        if self._stop_name == name:
            self._parser.setContentHandler(self._parent)
            return 1

    def characters(self, content):
        self._text.append(content)

    def parse(self, source):
        self._parser.setContentHandler(self)
        self._parser.parse(source)
