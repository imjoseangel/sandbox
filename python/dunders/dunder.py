class Color:
    """Make function name stand out"""
    BOLD = '\033[1m'
    END = '\033[0m'


def explore_dunder(any_var):
    """prints the dunder methods (magic methods) of any variable, along with documentation"""

    dir_list = dir(any_var)
    dunders = [fn for fn in dir_list if fn.startswith(
        "__") and fn.endswith("__")]
    for fn in dunders:
        print(Color.BOLD + fn + ":" + Color.END)
        print(f"{any_var.__getattribute__(fn).__doc__}\n")


msg = "Hello"
explore_dunder(msg)
