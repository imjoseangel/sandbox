#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import csv
import glob
import os
import xml.etree.ElementTree as ET
import xmltodict


def main():
    path = './xml'
    to_csv = []

    for filename in glob.glob(os.path.join(path, '*.xml')):

        tree = ET.parse(filename)
        xml_data = tree.getroot()
        xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

        data_dict = dict(xmltodict.parse(xmlstr))
        data_dict = data_dict['root']

        to_csv.append(data_dict)

    keys = to_csv[0].keys()

    with open('content.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)


if __name__ == '__main__':
    main()
