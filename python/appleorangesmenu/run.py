#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as pprint


def display_menu():
    """Display the menu options."""
    options = ["Oranges", "Mixed", "Exit"]

    for index, option in enumerate(options, 1):
        pprint(f"{index}. {option}")


loop = True

while loop:
    try:
        display_menu()
        box = input("Select the Apples Box [1-3]: ")
        match box:
            case "1":
                pprint(
                    ":tangerine: are in the :apple::tangerine:",
                    "box and :apple::tangerine: are in the :apple: box")
            case "2":
                pprint(
                    ":tangerine: are in the :apple: box and",
                    ":apple::tangerine: are in the :tangerine: box")
            case "3":
                break
            case _:
                pprint("Invalid option")
    except (KeyboardInterrupt, EOFError):
        pprint("Press 3 to exit")
