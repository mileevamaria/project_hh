from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from webapp.model import db, Vacancy, User, Favourite, Category, Skill
from webapp.forms import LoginForm, ProfileForm, RegistrationForm, ChangePasswordForm
import os
from webapp.statistic import set_statistic, get_languages, get_vacancies_count
import json

""" export FLASK_APP=webapp && FLASK_ENV=development && flask run """


def create_app():
    app = Flask(__name__)
    # app.config.from_pyfile('config.py')
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/lpproject'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        title = "Вакансии для разработчиков"
        page = request.args.get('page', 1, type=int)
        vacancies = Vacancy.query.paginate(page=page, per_page=20)

        if current_user.is_authenticated:
            favourite = Favourite.query.filter(
                Favourite.user_id == current_user.id).all()
            favourite_vacancy = []
            for favour in favourite:
                favourite_vacancy.append(favour.vacancy_id)
            return render_template('index.html', page_title=title, vacancies=vacancies, favourite=favourite_vacancy)
        else:
            return render_template('index.html', page_title=title, vacancies=vacancies)

    @app.route('/process-favourite/<int:id>', methods=['GET', 'POST'])
    @login_required
    def process_favourite(id):
        vacancy = Vacancy.query.get_or_404(id)
        vacancy_exists = Favourite.query.filter(Favourite.vacancy_id == vacancy.id,
                                                Favourite.user_id == current_user.id).first()
        if vacancy_exists:
            flash('Вы уже добавляли эту вакансию в избранное')
        else:
            vacancy_add = Favourite(
                vacancy_favourite=vacancy, user_favourite=current_user)
            db.session.add(vacancy_add)
            db.session.commit()
            flash('Вакансия добавлена в избранное')

        return redirect(url_for('index'))

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter(
                User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))

        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Регистрация'
        registration_form = RegistrationForm()
        return render_template('registration.html', page_title=title, form=registration_form)

    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data,
                            email=form.email.data, role='user')
            if form.first_name.data:
                new_user.first_name = form.first_name.data
            if form.last_name.data:
                new_user.last_name = form.last_name.data
            if form.city.data:
                new_user.city = form.city.data
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле {}: {}'.format(
                        getattr(form, field).label.text, error))

        return redirect(url_for('register'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ!'
        else:
            return 'Ты не админ!'

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        title = "Профиль пользователя"
        form = ProfileForm()
        user = User.query.filter(
            User.username == current_user.username).first()

        return render_template('profile.html', page_title=title, form=form, user=user)

    @app.route('/process-save-changes-person', methods=['POST'])
    def process_save_changes_person():
        form = ProfileForm()
        user = User.query.filter(
            User.username == current_user.username).first()
        if form.validate_on_submit():
            if form.first_name.data:
                user.first_name = form.first_name.data
            if form.last_name.data:
                user.last_name = form.last_name.data
            if form.city.data:
                user.city = form.city.data
            db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('profile'))

    @app.route('/profile/favourite', methods=['GET', 'POST'])
    @login_required
    def favourite():
        title = "Избранные вакансии"
        favourites = Favourite.query.filter(
            Favourite.user_id == current_user.id).all()
        return render_template('favourite.html', page_title=title, favourites=favourites)

    @app.route('/profile/change_password')
    def change_password():
        form = ChangePasswordForm()
        title = 'Изменить пароль'
        return render_template('change_password.html', page_title=title, form=form)

    @app.route('/process-change-password', methods=['POST'])
    def process_change_password():
        form = ChangePasswordForm()
        user = User.query.filter(
            User.username == current_user.username).first()
        if form.validate_on_submit() and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash('Пароль изменен')
            return redirect(url_for('profile'))

        else:
            if not user.check_password(form.old_password.data):
                flash('Неправильный текущий пароль')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        flash('Ошибка в поле {}: {}'.format(
                            getattr(form, field).label.text, error))

        return redirect(url_for('change_password'))

    @app.route('/process-delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def process_delete(id):
        favourite = Favourite.query.get_or_404(id)
        db.session.delete(favourite)
        db.session.commit()
        flash('Вакансия удалена из избранного')

        return redirect(url_for('favourite'))

    @app.route('/process-save-change-skills', methods=['POST'])
    def process_save_change_skills():
        form = ProfileForm()
        if form.validate_on_submit():
            user = User.query.filter(
                User.username == current_user.username).first()
            for skill in form.skills_nosql.data:
                skill.user.append(user)
                db.session.commit()

        flash('Изменения сохранены')
        return redirect(url_for('profile'))

    @app.route('/statistic', methods=['GET'])
    def statistic():
        title = 'Статистика вакансий'
        vacancies_count = get_vacancies_count()
        vacancies_count = json.dumps(vacancies_count)

        languages_stat = get_languages()
        lang_labels = json.dumps(languages_stat[0])
        lang_stat = json.dumps(languages_stat[1])

        return render_template('statistic.html', page_title=title, lang_labels=lang_labels, lang_stat=lang_stat, vacancies_count=vacancies_count)

    return app
