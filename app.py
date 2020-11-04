from flask import Flask, render_template, url_for, redirect
import subprocess as sp
import os
import socket
from time import strftime, tzname

app = Flask(__name__)


def run(command):
    output = sp.run(command, cwd=os.getcwd(), stdout=sp.PIPE)
    return output.stdout.decode('UTF-8')


@app.route('/')
def index():
    hostname = socket.gethostname()
    system_time = strftime("%H:%M:%S") + " (" + tzname[1] + ")"
    return render_template('index.html', system_time=system_time, hostname=hostname)


@app.route('/storage')
def storage():
    ls = run(['du', '-hcs /home/philipp/Cloud'])
    return render_template('storage.html', ls=ls)


@app.route('/commands')
def commands():
    return render_template('commands.html')


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
