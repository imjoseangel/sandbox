#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as pprint


def print_menu():
    """
    A function to print the menu options for the user interface.
    """

    pprint("1. Oranges")
    pprint("2. Mixed")
    pprint("3. Exit")


loop = True

while loop:
    try:
        print_menu()
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
