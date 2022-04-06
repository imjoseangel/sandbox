#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    url = "https://www.google.com"
    return render_template('index.html', iframe=url)


if __name__ == "__main__":
    app.run(debug=True)
