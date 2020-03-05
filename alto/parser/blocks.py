from alto.parser import HandlerBase

class Shape(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        self.shape_type = name
        self.attrs = dict(attrs)

class Block(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super().__init__(parser, parent, stop_name)

        self.components = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name in ("Polygon", "Ellipse", "Circle"):
            shape = Shape.as_sub_handler(self._parser, self, name)
            self.components.append(shape)

class String(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "String":
            self.attrs = dict(attrs)

class Space(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "SP":
            self.attrs = dict(attrs)

class Hyphen(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "HYP":
            self.attrs = dict(attrs)

class TextLine(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super().__init__(parser, parent, stop_name)

        self.components = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)

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

class TextBlock(Block):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "TextBlock":
            self.attrs = dict(attrs)
        elif name == "TextLine":
            line = TextLine.as_sub_handler(self._parser, self, name)
            line.startElement(name, attrs)
            self.components.append(line)

    def get_text_lines(self):
        return [component for component in self.components if type(component) == TextLine]

class BlockContainer(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super().__init__(parser, parent, stop_name)

        self.blocks = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)

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

class Illustration(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "Illustration":
            self.attrs = dict(attrs)

class GraphicalElement(HandlerBase):
    def startElement(self, name, attrs):
        super().startElement(name, attrs)

        if name == "GraphicalElement":
            self.attrs = dict(attrs)

class ComposedBlock(BlockContainer):
    pass
