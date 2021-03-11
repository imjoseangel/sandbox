import textwrap


def wrap(string, max_width):
    return "\n".join(textwrap.wrap(string, max_width))


if __name__ == '__main__':
    string, max_width = "ABCDEFGHIJKLIMNOQRSTUVWXYZ", 4
    result = wrap(string, max_width)
    print(result)
