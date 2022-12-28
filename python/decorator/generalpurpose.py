#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rich import print as rprint


def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        rprint(f'The positional arguments are {args}')
        rprint(f'The keyword arguments are {kwargs}')
        function_to_decorate(*args)
    return a_wrapper_accepting_arbitrary_arguments


@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    rprint("No arguments here.")


function_with_no_argument()
