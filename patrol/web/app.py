import logging

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route('/dq-checks/')
def dq_checks():
    return render_template('dq-checks.html')

@app.route('/connections/')
def connections():
    return render_template('connections.html')

@app.route('/rep-dq/')
def rep_dq():
    return render_template('rep-dq.html')
