from flask import Flask, render_template, url_for, redirect
import subprocess as sp
import os
import socket
from time import strftime, tzname
import shutil

app = Flask(__name__)
hostname = socket.gethostname()


def run(command):
    output = sp.run(command, cwd=os.getcwd(), stdout=sp.PIPE)
    return output.stdout.decode('UTF-8')


@app.route('/')
def index():
    uptime = run(['uptime', '-p'])
    uptime = uptime[3:]

    system_time = strftime("%H:%M:%S") + " (" + tzname[0] + ")"
    return render_template('index.html', system_time=system_time, hostname=hostname, uptime=uptime)


@app.route('/storage')
def storage():
    total, used, free = shutil.disk_usage("/")

    data = {"total": to_gib(total), "used": to_gib(used), "free": to_gib(free)}

    return render_template('storage.html', hostname=hostname, data=data)


def to_gib(number):
    return number // (2 ** 30)


@app.route('/commands')
def commands():
    return render_template('commands.html', hostname=hostname)


@app.route('/commands/chkrootkit_logs')
def chkrootkit_logs():
    command = ['cp', '-afv', '/var/log/chkrootkit/log.today', '/var/log/chkrootkit/log.expected']
    stdout = run(command)
    return render_template('command-output.html', stdout=stdout, command=command)


@app.route('/shutdown')
def shutdown():
    run(['shutdown', 'now'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
