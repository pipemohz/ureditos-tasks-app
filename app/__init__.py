from flask import Flask, redirect, render_template, url_for, session
from .test import server_is_up
from .modules import enrolling_moodle, send_sms_notifications, send_email_notifications
import logging
from datetime import datetime
from .config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
server_status = server_is_up()
year = datetime.today().year


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', status=server_status, tasks=session, year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)


@app.route('/moodle', methods=['POST'])
def moodle():
    logging.info('Execution of moodle module')
    enrolling_moodle()
    session['moodle'] = 'done'
    return redirect(url_for('index'))


@app.route('/mail', methods=['POST'])
def mail():
    logging.info('execute mail module.')
    send_email_notifications()
    session['email'] = 'done'
    return redirect(url_for('index'))


@app.route('/sms', methods=['POST'])
def sms():
    logging.info('Execution of sms module')
    send_sms_notifications()
    session['sms'] = 'done'
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
