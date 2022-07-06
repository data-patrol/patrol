import logging

from flask import Flask, render_template

import patrol.data_model as dm


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
    dq_check_runs = dm.session.query(dm.DQ_Check_Run).order_by(
            dm.DQ_Check_Run.start_time.desc()).limit(500)
    return render_template('rep-dq.html', dq_check_runs=dq_check_runs)
