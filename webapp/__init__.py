from flask import Flask, render_template, flash, redirect, url_for, request

from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from webapp.model import db, HeadHunterVacancy, Category, Skills, User, Favourite
from webapp.forms import LoginForm, ProfileForm, VacancyForm


""" export FLASK_APP=webapp && FLASK_ENV=development && flask run """


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        title = "Вакансии для разработчиков"
        page = request.args.get('page', 1, type=int)
        vacancies = HeadHunterVacancy.query.paginate(page=page, per_page=20)
        return render_template('index.html', page_title=title, vacancies=vacancies)

    @app.route('/process-favourite/<int:id>', methods=['GET', 'POST'])
    @login_required
    def process_favourite(id):
        vacancy = HeadHunterVacancy.query.get_or_404(id)
        vacancy_exists = Favourite.query.filter(Favourite.fav_vac_url == vacancy.vacancy_url,
                                                        Favourite.username == current_user.username).count()
        if vacancy_exists:
            flash('Вы уже добавляли эту вакансию в избранное')
        else:
            vacancy_add = Favourite(username=current_user.username, fav_vac_url=vacancy.vacancy_url,
                                    fav_vac_title=vacancy.vacancy_name)
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
            user = User.query.filter(User.username == form.username.data).first()
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
        user_info = User.query.filter(User.username == current_user.username).first()
        form = ProfileForm()
        return render_template('profile.html', page_title=title, form=form, user_info=user_info)

    @app.route('/profile/favourite', methods=['GET', 'POST'])
    @login_required
    def favourite():
        title = "Избранные вакансии"
        favourites = Favourite.query.filter(Favourite.username == current_user.username).all()
        return render_template('favourite.html', page_title=title, favourites=favourites)

    @app.route('/process-delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def process_delete(id):
        favourite = Favourite.query.get_or_404(id)
        db.session.delete(favourite)
        db.session.commit()
        flash('Вакансия удалена из избранного')

        return redirect(url_for('favourite'))

    return app
