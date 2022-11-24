import bz2
import json
import pathlib


def main():
    with open('pypicache.json', 'rb') as fp:
        filename = 'pypicache.json.bz2'
        with bz2.open(filename, 'wb') as wfp:
            wfp.write(bz2.compress(fp.read()))

        pathlib.Path(filename).unlink()


if __name__ == "__main__":
    main()
