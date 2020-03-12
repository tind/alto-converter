from alto.parser import HandlerBase

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

class Description(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super(Description, self).__init__(parser, parent, stop_name)
        self.processing_steps = []

    def startElement(self, name, attrs):
        super(Description, self).startElement(name, attrs)
        if name == "ocrProcessingStep":
            processing_step = OCRProcessingStep.as_sub_handler(self._parser, self, name)
            processing_step.startElement(name, attrs)
            self.processing_steps.append(processing_step)

    def endElement(self, name):
        if super(Description, self).endElement(name) is not None:
            return

        if name == "MeasurementUnit":
            self.measurement_unit = "".join(self._text)
        elif name == "fileName":
            self.file_name = "".join(self._text)

class OCRProcessingStep(HandlerBase):
    def endElement(self, name):
        if super(OCRProcessingStep, self).endElement(name) is not None:
            return

        if name == "processingDateTime":
            self.processing_date_time = "".join(self._text)
        elif name == "softwareName":
            self.software_name = "".join(self._text)
        elif name == "softwareVersion":
            self.software_version = "".join(self._text)

class Layout(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super(Layout, self).__init__(parser, parent, stop_name)

        self.pages = []

    def startElement(self, name, attrs):
        super(Layout, self).startElement(name, attrs)

        if name == "Layout":
            self.attrs = dict(attrs)
        elif name == "Page":
            page = Page.as_sub_handler(self._parser, self, name)
            page.startElement(name, attrs)
            self.pages.append(page)

class Page(HandlerBase):
    def startElement(self, name, attrs):
        super(Page, self).startElement(name, attrs)

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

class BlockContainer(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super(BlockContainer, self).__init__(parser, parent, stop_name)

        self.blocks = []

    def startElement(self, name, attrs):
        super(BlockContainer, self).startElement(name, attrs)

        if name == "TextBlock":
            text_block = TextBlock.as_sub_handler(self._parser, self, name)
            text_block.startElement(name, attrs)
            self.blocks.append(text_block)
        elif name == "Illustration":
            illustration = Illustration.as_sub_handler(self._parser, self, name)
            illustration.startElement(name, attrs)
            self.blocks.append(illustration)
        elif name == "GraphicalElement":
            graphical_element = GraphicalElement.as_sub_handler(self._parser, self, name)
            graphical_element.startElement(name, attrs)
            self.blocks.append(graphical_element)
        elif name == "ComposedBlock":
            composed_block = ComposedBlock.as_sub_handler(self._parser, self, name)
            composed_block.attrs = dict(attrs)
            self.blocks.append(composed_block)

    def get_blocks_by_name(self, type_name):
        return [block for block in self.blocks if type(block).__name__ == type_name]

class PageSpace(BlockContainer):
    def startElement(self, name, attrs):
        super(PageSpace, self).startElement(name, attrs)

        if name == self._stop_name:
            self.attrs = dict(attrs)

class Block(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super(Block, self).__init__(parser, parent, stop_name)

        self.components = []

    def startElement(self, name, attrs):
        super(Block, self).startElement(name, attrs)

        if name in ("Polygon", "Ellipse", "Circle"):
            shape = Shape.as_sub_handler(self._parser, self, name)
            self.components.append(shape)

class TextBlock(Block):
    def startElement(self, name, attrs):
        super(TextBlock, self).startElement(name, attrs)

        if name == "TextBlock":
            self.attrs = dict(attrs)
        elif name == "TextLine":
            line = TextLine.as_sub_handler(self._parser, self, name)
            line.startElement(name, attrs)
            self.components.append(line)

    def get_text_lines(self):
        return [component for component in self.components if type(component) == TextLine]

class Shape(HandlerBase):
    def startElement(self, name, attrs):
        super(Shape, self).startElement(name, attrs)

        self.shape_type = name
        self.attrs = dict(attrs)


class Illustration(HandlerBase):
    def startElement(self, name, attrs):
        super(Illustration, self).startElement(name, attrs)

        if name == "Illustration":
            self.attrs = dict(attrs)

class GraphicalElement(HandlerBase):
    def startElement(self, name, attrs):
        super(GraphicalElement, self).startElement(name, attrs)

        if name == "GraphicalElement":
            self.attrs = dict(attrs)

class ComposedBlock(BlockContainer):
    pass

class TextLine(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super(TextLine, self).__init__(parser, parent, stop_name)

        self.components = []

    def startElement(self, name, attrs):
        super(TextLine, self).startElement(name, attrs)

        if name == "TextLine":
            self.attrs = dict(attrs)
        elif name == "String":
            string = String.as_sub_handler(self._parser, self, name)
            string.startElement(name, attrs)
            self.components.append(string)
        elif name == "SP":
            space = Space.as_sub_handler(self._parser, self, name)
            space.startElement(name, attrs)
            self.components.append(space)
        elif name == "HYP":
            hyphen = Hyphen.as_sub_handler(self._parser, self, name)
            hyphen.startElement(name, attrs)
            self.components.append(hyphen)

    def get_strings(self):
        return [component for component in self.components if type(component) == String]

class String(HandlerBase):
    def startElement(self, name, attrs):
        super(String, self).startElement(name, attrs)

        if name == "String":
            self.attrs = dict(attrs)

class Space(HandlerBase):
    def startElement(self, name, attrs):
        super(Space, self).startElement(name, attrs)

        if name == "SP":
            self.attrs = dict(attrs)

class Hyphen(HandlerBase):
    def startElement(self, name, attrs):
        super(Hyphen, self).startElement(name, attrs)

        if name == "HYP":
            self.attrs = dict(attrs)

