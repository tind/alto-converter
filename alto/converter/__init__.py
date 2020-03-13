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

from alto.parser.handler import (ComposedBlock,
                                 TextBlock,
                                 TextLine,
                                 String,
                                 Hyphen)

def prepare_line(text_line):
    line = {"id": text_line.get_id(),
            "type": "text_line",
            "box": text_line.get_box(),
            "components": []}
    for line_component in text_line.components:
        e = {"id": line_component.get_id(),
             "box": line_component.get_box()}
        if type(line_component) == String:
            e.update({"type": "string",
                      "content": line_component.attrs.get("CONTENT")})
        elif type(line_component) == Hyphen:
            e.update({"type": "hyphen",
                      "content": line_component.attrs.get("CONTENT")})
        else:
            continue
        line["components"].append(e)
    return line

def prepare_container(container):
    c = {"id": container.get_id(),
         "type": "container",
         "box": container.get_box(),
         "blocks": []}
    for container_block in container.blocks:
        if type(container_block) == TextBlock:
            block = {"id": container_block.get_id(),
                     "type": "text_block",
                     "lang": container_block.attrs.get("language") or container_block.attrs.get("LANG"),
                     "box": container_block.get_box(),
                     "lines": []}
            for block_component in container_block.components:
                if type(block_component) != TextLine:
                    continue
                block["lines"].append(prepare_line(block_component))
            c["blocks"].append(block)
        elif type(container_block) == ComposedBlock:
            c["blocks"].append(prepare_container(container_block))
    return c

def prepare_alto(alto):
    """
    Prepares a simple dictionary structure, intended for use in templates.

    """
    hocr = {"file_name": getattr(alto.description, "file_name", "file"),
            "system": [(step.software_name, step.software_version) for step in alto.description.processing_steps]}

    hocr["pages"] = []
    for page in alto.layout.pages:
        p = {"width": page.attrs.get("WIDTH"),
             "height": page.attrs.get("HEIGHT"),
             "id": page.get_id()}
        for space in "top_margin", "print_space", "bottom_margin":
            s = getattr(page, space, None)
            if s is not None:
                p[space] = prepare_container(s)
        hocr["pages"].append(p)
    return hocr
