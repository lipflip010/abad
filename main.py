# main.py
import os
import shutil
from time import strftime, tzname

from flask import Blueprint, render_template
from flask_login import login_required

from utils import run, to_gib

main = Blueprint('main', __name__)


@main.context_processor
def get_current_user():
    from abad import hostname
    return {"hostname": hostname}


@main.route('/')
def index():
    uptime = run(['uptime', '-p'])
    uptime = uptime[3:-1]

    system_time = strftime("%H:%M:%S") + " (" + tzname[0] + ")"
    return render_template('index.html', system_time=system_time, uptime=uptime)


@main.route('/storage')
def storage():
    total, used, main_free = shutil.disk_usage("/")
    data = {"main": to_gib(main_free)}

    if os.path.exists("/media/USBdrive"):
        total1, used1, usbdrive_free = shutil.disk_usage("/media/USBdrive")
        data["usbdrive"] = to_gib(usbdrive_free)

    return render_template('storage.html', data=data)


@main.route('/commands')
@login_required
def commands():
    return render_template('commands.html')


@main.route('/commands/chkrootkit_logs')
@login_required
def chkrootkit_logs():
    command = ['cp', '-afv', '/var/log/chkrootkit/log.today', '/var/log/chkrootkit/log.expected']
    stdout = run(command)
    return render_template('command-output.html', stdout=stdout, command=command)


@main.route('/shutdown')
def shutdown():
    run(['shutdown', 'now'])
