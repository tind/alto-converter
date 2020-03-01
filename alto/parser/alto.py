from alto.parser import HandlerBase
from alto.parser.description import Description
from alto.parser.layout import Layout

class Alto(HandlerBase):
    def startElement(self, name, attrs):
        if name == "Description":
            self.description = Description.as_sub_handler(self._parser, self, name)
            self.description.startElement(name, attrs)
        elif name == "Styles":
            styles = HandlerBase.as_sub_handler(self._parser, self, name)
            styles.startElement(name, attrs)
        elif name == "Layout":
            self.layout = Layout.as_sub_handler(self._parser, self, name)
            self.layout.startElement(name, attrs)
