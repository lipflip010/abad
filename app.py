from flask import Flask, render_template
import subprocess as sp
import os

app = Flask(__name__)


def run(command):
    return sp.check_output(command,cwd=os.getcwd())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return run(['date', '+%T'])


@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
