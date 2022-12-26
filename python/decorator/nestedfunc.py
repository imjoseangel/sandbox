#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich import print as rprint


def print_message(message):
    "Enclosing Function"
    def message_sender() -> str:
        "Nested Function"
        rprint(message)

    message_sender()


print_message("Some random message")
