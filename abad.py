from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import subprocess as sp
import os
import socket
from time import strftime, tzname
import shutil
from models import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

hostname = socket.gethostname()

"""
new_user = User(email="admin@palbers.de", password="pbkdf2:sha256:150000$tN0vzQhN$6ecb5bccea45be4f349caf081b4d50da440b53f7ea42193c40de7bf5bd58e39c")

# add the new user to the database
db.session.add(new_user)
db.session.commit()
"""


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


def run(command):
    output = sp.run(command, cwd=os.getcwd(), stdout=sp.PIPE)
    return output.stdout.decode('UTF-8')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('storage'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    uptime = run(['uptime', '-p'])
    uptime = uptime[3:-1]

    system_time = strftime("%H:%M:%S") + " (" + tzname[0] + ")"
    return render_template('index.html', system_time=system_time, hostname=hostname, uptime=uptime)


@app.route('/storage')
def storage():
    total, used, main_free = shutil.disk_usage("/")
    data = {"main": to_gib(main_free)}

    if os.path.exists("/media/USBdrive"):
        total1, used1, usbdrive_free = shutil.disk_usage("/media/USBdrive")
        data["usbdrive"] = to_gib(usbdrive_free)

    return render_template('storage.html', hostname=hostname, data=data)


def to_gib(number):
    return number // (2 ** 30)


@app.route('/commands')
@login_required
def commands():
    return render_template('commands.html', hostname=hostname)


@app.route('/commands/chkrootkit_logs')
@login_required
def chkrootkit_logs():
    command = ['cp', '-afv', '/var/log/chkrootkit/log.today', '/var/log/chkrootkit/log.expected']
    stdout = run(command)
    return render_template('command-output.html', stdout=stdout, command=command)


@app.route('/shutdown')
def shutdown():
    run(['shutdown', 'now'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
