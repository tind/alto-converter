from alto.parser import HandlerBase
from alto.parser.blocks import BlockContainer

class PageSpace(BlockContainer):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == self._stop_name:
            self.attrs = dict(attrs)

class Page(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)
        
        if name == "Page":
            self.attrs = dict(attrs)
        elif name == "TopMargin":
            self.top_margin = PageSpace.as_sub_handler(self._parser, self, name)
            self.top_margin.startElement(name, attrs)
        elif name == "LeftMargin":
            self.left_margin = PageSpace.as_sub_handler(self._parser, self, name)
            self.left_margin.startElement(name, attrs)
        elif name == "RightMargin":
            self.right_margin = PageSpace.as_sub_handler(self._parser, self, name)
            self.right_margin.startElement(name, attrs)
        elif name == "BottomMargin":
            self.bottom_margin = PageSpace.as_sub_handler(self._parser, self, name)
            self.bottom_margin.startElement(name, attrs)
        elif name == "PrintSpace":
            self.print_space = PageSpace.as_sub_handler(self._parser, self, name)
            self.print_space.startElement(name, attrs)

class Layout(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super().__init__(parser, parent, stop_name)

        self.pages = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "Layout":
            self.attrs = dict(attrs)
        elif name == "Page":
            page = Page.as_sub_handler(self._parser, self, name)
            page.startElement(name, attrs)
            self.pages.append(page)
