#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def decorator_with_arguments(function):
    def wrapper_accepting_arguments(arg1, arg2):
        rprint(f"My arguments are {arg1}, {arg2}")
        function(arg1, arg2)
    return wrapper_accepting_arguments


@decorator_with_arguments
def cities(city_one, city_two) -> None:
    rprint(f"Cities I love are {city_one} and {city_two}")


cities("Madrid", "Amersfoort")
