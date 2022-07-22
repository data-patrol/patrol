import logging

from datetime import datetime
from flask import Flask, request, render_template
import pandas as pd

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
    session = dm.Session()
    dq_check_runs = session.query(dm.DQ_Check_Run).order_by(
            dm.DQ_Check_Run.start_time.desc()).limit(5000)
    session.close()

    return render_template('rpt-detailed.html', dq_check_runs=dq_check_runs)

@app.route('/check-details/')
def check_details():
    guid = request.args.get('guid')
    session = dm.Session()
    dq_check_run = session.query(dm.DQ_Check_Run).filter_by(guid=guid).all()[0]
    session.close()

    df_report = pd.read_table(dq_check_run.report_file, delimiter='\t')

    return render_template('check-details.html', column_names=df_report.columns.values, 
                            row_data=list(df_report.values.tolist()), zip=zip)

