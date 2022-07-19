import logging

from datetime import datetime
from flask import Flask, render_template

import patrol.data_model as dm


app = Flask(__name__)

@app.route("/")
@app.route('/checks/')
def checks():
    return render_template('checks.html')

@app.route('/connections/')
def connections():
    return render_template('connections.html')

@app.route('/rpt-detailed/')
def rpt_detailed():
    dq_check_runs = dm.session.query(dm.DQ_Check_Run).order_by(
            dm.DQ_Check_Run.start_time.desc()).limit(5000)
    return render_template('rpt-detailed.html', datetime=datetime, dq_check_runs=dq_check_runs)

@app.route('/check-details/')
def check_details():
    return render_template('check-details.html')

