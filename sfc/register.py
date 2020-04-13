#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from dataclasses import dataclass, field
from typing import Dict

from django.template import Template
from django.template.defaulttags import LoadNode


class ComponentTemplates:
    def __init__(self, template: Template):
        self.name = template.name
        self.origin = template.origin
        self.css = ScfNode('style', template)
        self.html = ScfNode('template', template)
        self.js = ScfNode('script', template)

        dir_, _, file = self.name.rpartition(os.path.sep)
        dir_ = os.path.join(*dir_.split(os.path.sep)[::-1])
        self.file_name = os.path.join(dir_, file)


class ScfNode:
    def __init__(self, tag: str, template: Template):
        self.tag = tag
        self.data = None
        self.load(template.source)
        self.name = template.name
        self.deps = [r.token.contents.split(' ')[-1]
                     for r in template.compile_nodelist() if isinstance(r, LoadNode)]

    def render(self):
        return self.data.strip("\n")

    def load(self, template_str):
        regex = f'<{self.tag}>(.*)</{self.tag}>'
        self.data = "".join(re.compile(regex, re.S).findall(template_str))


@dataclass
class Registry:
    templates: Dict[str, ComponentTemplates] = field(default_factory=dict)
    queue: set = field(default_factory=set)

    def register(self, template: Template):
        self.templates[template.name] = ComponentTemplates(template)

    def get(self, name):
        return self.templates.get(name)

    def get_html(self, name):
        return self.get(name).html.render()


registry = Registry()
