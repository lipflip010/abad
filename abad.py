import socket

from flask import Flask
from flask_login import LoginManager

from models import db, User

hostname = socket.gethostname()


def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile(config_file)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth parts of app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


"""
new_user = User(email="admin@palbers.de", password="pbkdf2:sha256:150000$tN0vzQhN$6ecb5bccea45be4f349caf081b4d50da440b53f7ea42193c40de7bf5bd58e39c")

# add the new user to the database
db.session.add(new_user)
db.session.commit()
"""

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=8080)
