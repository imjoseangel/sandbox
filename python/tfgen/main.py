#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Terraform template generator
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import json
import re
from jinja2 import FileSystemLoader, Environment


def cleanregex(jinput: str) -> str:
    """Custom filter"""
    pattern = '(?m)\\(\\?=.{\\d+,\\d+}\\$\\)|\\(\\?!\\.\\*--\\)'
    return re.sub(re.compile(pattern), "", jinput)


def main():
    """
    Main function
    """

    with open('resourceDefinition.json', encoding='utf-8') as json_file:
        definition = json.load(json_file)

    with open('resourceDefinition_out_of_docs.json', encoding='utf-8') as jsonout_file:
        definitionout = json.load(jsonout_file)

    data = definition + definitionout

    loader = FileSystemLoader('templates')
    env = Environment(autoescape=True, loader=loader)

    env.filters['cleanRegex'] = cleanregex
    maintftemp = env.get_template('main.j2')
    outputtftemp = env.get_template('outputs.j2')
    maintemplate = maintftemp.render(data=data)
    outputtemplate = outputtftemp.render(data=data)

    with open("main.tf", "w", encoding="utf-8") as maintf:
        maintf.write(maintemplate)
        maintf.write("\n")
        maintf.close()

    with open("outputs.tf", "w", encoding="utf-8") as outputtf:
        outputtf.write(outputtemplate)
        outputtf.write("\n")
        outputtf.close()


if __name__ == '__main__':
    main()
