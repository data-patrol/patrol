import datetime
import logging

from flask import Flask

from patrol.executors import BaseEx

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
