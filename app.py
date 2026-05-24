# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>DevOps Project - Mahesh Babu</h1>"


@app.route("/health")
def health():
    return {"status": "working"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
