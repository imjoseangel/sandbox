#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Template
"""

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
from asyncio import threads

from dataclasses import dataclass
import logging
import os
import sys
import time
from waitress import serve
from flask import Flask, request
from sklearn import tree

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.resources import (SERVICE_NAME, SERVICE_NAMESPACE,
                                         SERVICE_INSTANCE_ID, Resource)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create(
            {
                SERVICE_NAME: "Kubernetes Test",
                # ----------------------------------------
                # Setting role name and role instance
                # ----------------------------------------
                SERVICE_NAMESPACE: "kubernetes",
                SERVICE_INSTANCE_ID: "k8stest",
                # ----------------------------------------------
                # Done setting role name and role instance
                # ----------------------------------------------
            }
        )
    )
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(AzureLogHandler(
    connection_string="InstrumentationKey=<your instrumentation key"))

exporter = AzureMonitorTraceExporter.from_connection_string(
    "InstrumentationKey=<your instrumentation key>"
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


@ dataclass
class RunJob:

    @ staticmethod
    def animation():
        anime = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + anime[i % len(anime)])
            sys.stdout.flush()

    @ staticmethod
    def get_running():

        try:

            with tracer.start_as_current_span("run"):

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
                logger.info(request.json)

                result = classifier.predict(
                    [[request.json['size'], request.json['roughness']]])

                # Output is apple for [120, 1]
                logger.info({result[0]})
                return f"{{'{result[0]}'}}"

        except KeyError as e:
            logger.error(e)
            return (f"Error: Incorrect {e} \n\n"
                    f"{syntax}")

        except TypeError as e:
            logger.error(e)
            return (f"Error: Incorrect {e} \n\n"
                    f"{syntax}")


app = Flask(__name__)
jobrequests = RunJob()


@ app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        with tracer.start_as_current_span("home"):
            logger.info("Running ML model")
            return jobrequests.get_running()
    else:
        return 'healthy'


def main():
    """
    Main function
    """
    os.system('clear')

    logging.info("""
██╗  ██╗ █████╗ ███████╗████████╗███████╗███████╗████████╗
██║ ██╔╝██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
█████╔╝ ╚█████╔╝███████╗   ██║   █████╗  ███████╗   ██║
██╔═██╗ ██╔══██╗╚════██║   ██║   ██╔══╝  ╚════██║   ██║
██║  ██╗╚█████╔╝███████║   ██║   ███████╗███████║   ██║
╚═╝  ╚═╝ ╚════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝
                                                            """)
    try:
        serve(app, port="8080", threads=25)
    except OSError as e:
        logging.error(e)


if __name__ == '__main__':
    main()
