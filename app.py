from flask import Flask, render_template
import subprocess as sp
import os

app = Flask(__name__)


def run(command):
    return sp.check_output(command,cwd=os.getcwd())


@app.route('/')
def index():
    st = run(['date', '+%T'])
    return render_template('index.html',system_time=st)


@app.route('/time')
def system_time():
    return


@app.route('/ls')
def ls():
    return run(['ls', '-l'])


@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
