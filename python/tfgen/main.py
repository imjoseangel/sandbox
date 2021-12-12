#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
from jinja2 import Template


def main():
    """
    Main function
    """

    with open('resourceDefinition.json') as json_file:
        data = json.load(json_file)

    with open('templates/main.j2', 'r', encoding="utf-8") as open_file:
        template = Template(open_file.read())

    f = open("main.tf", "w", encoding="utf-8")
    f.write(template.render(data=data))
    f.write("\n")
    f.close()


if __name__ == '__main__':
    main()
