#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print as rprint


def decorator_maker_with_arguments(decorator_arg1, decorator_arg2, decorator_arg3):
    def decorator(func):
        def wrapper(function_arg1, function_arg2, function_arg3):
            "This is the wrapper function"
            rprint(f"The wrapper can access all the variables\n"
                   f"\t- from the decorator maker: {decorator_arg1} "
                   f"{decorator_arg2} {decorator_arg3}\n"
                   f"\t- from the function call: {function_arg1} {function_arg2} "
                   f"{function_arg3}\n"
                   f"and pass them to the decorated function")
            return func(function_arg1, function_arg2, function_arg3)

        return wrapper

    return decorator


pandas = "Pandas"


@decorator_maker_with_arguments(pandas, "Numpy", "Scikit-learn")
def decorated_function_with_arguments(function_arg1, function_arg2, function_arg3):
    print(f"This is the decorated function and it only knows about its arguments: {function_arg1}"
          f" {function_arg2} {function_arg3}")


decorated_function_with_arguments(pandas, "Science", "Tools")
