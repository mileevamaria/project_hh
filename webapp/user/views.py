from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for
from flask import Blueprint

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db

blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('vacancy.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(
            User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('vacancy.index'))

    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('vacancy.index'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('vacancy.index'))
    title = 'Регистрация'
    registration_form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=registration_form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
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
        return redirect(url_for('user.login'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text, error))

    return redirect(url_for('user.register'))
