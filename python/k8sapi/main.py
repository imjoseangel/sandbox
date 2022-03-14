#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from dataclasses import dataclass
import logging
import os
import sys
import time
from waitress import serve
from flask import Flask, request
from sklearn import tree


def animation():
    anime = "|/-\\"
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write("\r" + anime[i % len(anime)])
        sys.stdout.flush()


@dataclass
class RunJob:

    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%d-%b-%y %H:%M:%S",
    )

    @staticmethod
    def animation():
        anime = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + anime[i % len(anime)])
            sys.stdout.flush()

    @staticmethod
    def get_running():

        try:

            syntax = ("Syntax:\n"
                      "-------\n\n"
                      "BODY POST:\n\n"
                      '{\n'
                      '"size": "<size>",\n'
                      '"roughness": "<roughness>"\n'
                      '}')

            # logging.info(request.environ)
            # features = [[155, "rough"], [180, "rough"], [135, "smooth"],
            # [110, "smooth"], etc]  # Input to classifier
            features = [[155, 0], [180, 0], [135, 1], [110, 1], [300, 0], [320, 0],
                        [350, 1], [380, 1]]  # scikit-learn requires real-valued features

            # labels = ["orange", "orange", "apple", "apple", "melon", "melon",
            # "watermelon", "watermelon"]  # output values
            labels = ['🍊', '🍊', '🍎', '🍎', '🍈', '🍈', '🍉', '🍉']

            # Training classifier
            classifier = tree.DecisionTreeClassifier()  # using decision tree classifier
            classifier = classifier.fit(
                features, labels)  # Find patterns in data

            # Making predictions
            logging.info(request.json)

            result = classifier.predict(
                [[request.json['size'], request.json['roughness']]])

            # Output is apple for [120, 1]
            logging.info({result[0]})
            return f"{{'{result[0]}'}}"

        except KeyError as e:
            logging.error(e)
            return (f"Error: Incorrect {e} \n\n"
                    f"{syntax}")

        except TypeError as e:
            logging.error(e)
            return (f"Error: Incorrect {e} \n\n"
                    f"{syntax}")


app = Flask(__name__)
jobrequests = RunJob()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        return jobrequests.get_running()
    else:
        logging.info('GET Method not allowed')
        return 'GET Method not allowed'


def main():
    """
    Main function
    """
    os.system('clear')

    print("""██╗  ██╗ █████╗ ███████╗████████╗███████╗███████╗████████╗
██║ ██╔╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
█████╔╝ ╚█████╔╝███████╗   ██║   █████╗  ███████╗   ██║
██╔═██╗ ██╔══██╗╚════██║   ██║   ██╔══╝  ╚════██║   ██║
██║  ██╗╚█████╔╝███████║   ██║   ███████╗███████║   ██║
╚═╝  ╚═╝ ╚════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝
                                                            """)
    try:
        serve(app, port="8080")
    except OSError as e:
        logging.error(e)


if __name__ == '__main__':
    main()
