from flask import Flask, render_template
import subprocess as sp
import os

app = Flask(__name__)


def run(command):
    output = sp.run(command, cwd=os.getcwd(), stdout=sp.PIPE)
    return output.stdout.decode('UTF-8')


@app.route('/')
def index():
    system_time = run(['date', '+%T'])
    return render_template('index.html', system_time=system_time)


@app.route('/storage')
def storage():
    ls = run(['du', '-hcs /home/philipp/Cloud'])
    return render_template('storage.html', ls=ls)


@app.route('/shutdown')
def shutdown():
    run(['shutdown', 'now'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
