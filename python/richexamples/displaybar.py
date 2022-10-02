#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from rich.progress import track


def process_data():
    sleep(0.02)


for _ in track(range(100), description='[green]Processing data'):
    process_data()
