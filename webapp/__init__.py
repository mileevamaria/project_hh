from flask import Flask
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate

from webapp.user.views import blueprint as user_blueprint
from webapp.profile.views import blueprint as profile_blueprint
from webapp.vacancy.views import blueprint as vacancy_blueprint
from webapp.statistic.views import blueprint as statistic_blueprint

from webapp.db import db
from webapp.user.models import User

""" export FLASK_APP=webapp && FLASK_ENV=development && flask run """


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(vacancy_blueprint)
    app.register_blueprint(statistic_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ!'
        else:
            return 'Ты не админ!'

    return app
