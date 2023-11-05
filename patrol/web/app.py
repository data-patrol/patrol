import logging

from datetime import datetime
from flask import Flask, request, render_template
import pandas as pd

import patrol.data_model as dm
from api.dq_checks import dq_endpoints_bp
from api.dq_check_run import dq_run_endpoints_bp
from api.check_registry import dq_run_endpoints_bp
from api.process_log import process_log_endpoints_bp


app = Flask(__name__)

app.register_blueprint(dq_endpoints_bp, url_prefix='/api')
app.register_blueprint(dq_run_endpoints_bp, url_prefix='/api')
app.register_blueprint(check_registry_endpoints_bp, url_prefix='/api')
app.register_blueprint(process_log_endpoints_bp, url_prefix='/api')

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
    dq_check_runs = session.query(dm.DQCheckRun, dm.DQCheck).join(dm.DQCheck, 
        dm.DQCheckRun.check_id == dm.DQCheck.check_id).order_by(
            dm.DQCheckRun.start_time.desc()).limit(5000)
    session.close()

    return render_template('rpt-detailed.html', dq_check_runs=dq_check_runs)

@app.route('/check-details/')
def check_details():
    guid = request.args.get('guid')
    step = request.args.get('step')
    session = dm.Session()
    dq_check_run = session.query(dm.DQCheckRun).filter_by(guid=guid, step_seq=step).all()[0]
    session.close()

    df_report = pd.read_table(dq_check_run.report_file, delimiter='\t')

    return render_template('check-details.html', column_names=df_report.columns.values, 
                            row_data=list(df_report.values.tolist()), zip=zip)

