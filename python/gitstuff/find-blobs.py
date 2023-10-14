import zlib
import sys

for line in sys.stdin:
    line = line.strip()
    filename = f".git/objects/{line[0:2]}/{line[2:]}"

    try:

        with open(filename, "rb") as f:
            contents = zlib.decompress(f.read())
            if contents.startswith(b"blob"):
                print(line)

    except FileNotFoundError:
        pass
