from xml.sax.handler import ContentHandler

class HandlerBase(ContentHandler, object):
    num = 0

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

    def get_id(self):
        if "ID" in self.attrs:
            return self.attrs["ID"]

        num = HandlerBase.num
        HandlerBase.num += 1
        return "{}_{}".format(type(self).__name__, num)

    def get_box(self):
        try:
            right = int(self.attrs["WIDTH"]) + int(self.attrs["HPOS"])
            bottom = int(self.attrs["HEIGHT"]) + int(self.attrs["VPOS"])
        except KeyError:
            return ""

        elements = ["bbox", self.attrs["HPOS"], self.attrs["VPOS"], right, bottom]
        if "WC" in self.attrs:
            elements.append("; x_wconf " + str(float(self.attrs["WC"]) * 100))

        return " ".join([str(e) for e in elements])

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
