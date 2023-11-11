#!/bin/python

import argparse
import os
import http.server

parser = argparse.ArgumentParser()
parser.add_argument('root', type=str,
                    help='The root directory to walk.')


def main(args):
    """Prints the files that are inside the container, rooted at the first argument."""
    for dirpath, _, files in os.walk(args.root):
        for f in files:
            print(os.path.join(dirpath, f))


def run(server_class=http.server.HTTPServer, handler_class=http.server.SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    main(parser.parse_args())
    run()
