from flask import Flask, render_template
from webapp.model import db, HeadHunterVacancy, Category, Skills


""" export FLASK_APP=webapp && FLASK_ENV=development && flask run """


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = "Вакансии для разработчиков"
        vacancies = HeadHunterVacancy.query.all()
        categories = Category.query.all()
        skills = Skills.query.all()
        return render_template('index.html', page_title=title, vacancies=vacancies,
                               categories=categories, skills=skills)

    return app
