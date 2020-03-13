#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 TIND
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.sax import make_parser
from xml.sax.saxutils import prepare_input_source

from jinja2 import Environment, PackageLoader, select_autoescape

from alto.parser.handler import Alto
from alto.converter import prepare_alto

def main():
    parser = make_parser()
    alto = Alto(parser)

    with open("alto.xml", "r") as f:
        source = prepare_input_source(f)
        alto.parse(source)

    print("Parsed")

    hocr = prepare_alto(alto)

    print("Converted")

    env = Environment(loader=PackageLoader("alto.converter", "templates"),
                      autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template("hocr.html")
    print(template.render(language={"lang": "en"}, hocr=hocr))

if __name__ == "__main__":
    main()
