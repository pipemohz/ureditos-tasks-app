from flask import Flask, redirect, render_template, url_for, session
from .test import is_server_up
import logging
from datetime import datetime
from .config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
year = datetime.today().year


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    server_up = is_server_up()
    return render_template('index.html', server_up=server_up, tasks=session, year=year)


@app.route('/about')
def about():
    return render_template('about.html', year=year)


@app.route('/moodle/<string:mode>', methods=['POST'])
def moodle(mode):
    logging.info('Execution of moodle module')
    if mode == 'commercial':
        from .commercial import enrolling_moodle
        session[f'{mode}_moodle'] = 'done'

    else:
        from .service import enrolling_moodle
        session[f'{mode}_moodle'] = 'done'

    enrolling_moodle()
    return redirect(url_for('index'))


@app.route('/mail/<string:mode>', methods=['POST'])
def mail(mode):
    logging.info('execute mail module.')
    if mode == 'commercial':
        from .commercial import send_email_notifications
        session[f'{mode}_email'] = 'done'
    else:
        from .service import send_email_notifications
        session[f'{mode}_email'] = 'done'

    send_email_notifications()
    return redirect(url_for('index'))


@app.route('/sms/<string:mode>', methods=['POST'])
def sms(mode):
    logging.info('Execution of sms module')
    if mode == 'commercial':
        from .commercial import send_sms_notifications
        session[f'{mode}_sms'] = 'done'
    else:
        from .service import send_sms_notifications
        session[f'{mode}_sms'] = 'done'

    send_sms_notifications()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
