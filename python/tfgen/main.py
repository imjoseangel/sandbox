#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
import re
from jinja2 import FileSystemLoader, Environment


def cleanRegex(input):
    """Custom filter"""
    pattern = re.compile('(?m)\\(\\?=.{\\d+,\\d+}\\$\\)|\\(\\?!\\.\\*--\\)')
    return re.sub(pattern, '', input)


def main():
    """
    Main function
    """

    with open('resourceDefinition.json') as json_file:
        data = json.load(json_file)

    # with open('templates/main.j2', 'r', encoding="utf-8") as open_file:

    loader = FileSystemLoader('templates')
    env = Environment(autoescape=True, loader=loader)

    env.filters['cleanRegex'] = cleanRegex
    temp = env.get_template('main.j2')
    maintemplate = temp.render(data=data)

    f = open("main.tf", "w", encoding="utf-8")
    f.write(maintemplate)
    f.write("\n")
    f.close()


if __name__ == '__main__':
    main()
