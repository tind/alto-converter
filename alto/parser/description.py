from alto.parser import HandlerBase

class OCRProcessingStep(HandlerBase):
    def endElement(self, name):
        if super().endElement(name) is not None:
            return

        if name == "processingDateTime":
            self.processing_date_time = "".join(self._text)
        elif name == "softwareName":
            self.software_name = "".join(self._text)
        elif name == "softwareVersion":
            self.software_version = "".join(self._text)

class Description(HandlerBase):
    def __init__(self, parser, parent, stop_name):
        super().__init__(parser, parent, stop_name)
        self.processing_steps = []

    def startElement(self, name, attrs):
        super().startElement(name, attrs)
        if name == "ocrProcessingStep":
            processing_step = OCRProcessingStep.as_sub_handler(self._parser, self, name)
            processing_step.startElement(name, attrs)
            self.processing_steps.append(processing_step)

    def endElement(self, name):
        if super().endElement(name) is not None:
            return

        if name == "MeasurementUnit":
            self.measurement_unit = "".join(self._text)
        elif name == "fileName":
            self.file_name = "".join(self._text)
