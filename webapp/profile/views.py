from flask import render_template, flash, redirect, url_for, request
from flask import Blueprint
from flask_login import current_user, login_required
from sqlalchemy import or_

from webapp.profile.forms import ChangePasswordForm, ProfileForm
from webapp.profile.models import Favourite
from webapp.profile.profile_skills import *
from webapp.user.models import User
from webapp.vacancy.models import Vacancy, Skill, Category, ProfessionalArea
from webapp.db import db

blueprint = Blueprint('profile', __name__)


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    title = "Профиль пользователя"
    form = ProfileForm()
    user = User.query.filter(
        User.id == current_user.id).first()

    skills_base = []
    for item in user.user_skill:
        skills_base.append(item.id)

    areas_base = []
    for item in user.user_area:
        areas_base.append(item.id)
    print(areas_base)

    area_page = ProfessionalArea.query.all()
    skills_page_lang = Category.query.filter(
        Category.id == 1).first().catskill
    skills_page_db = Category.query.filter(
        Category.id == 2).first().catskill
    skills_page_frame = Category.query.filter(
        Category.id == 3).first().catskill
    skills_page_webprot = Category.query.filter(
        Category.id == 4).first().catskill
    skills_page_search = Category.query.filter(
        Category.id == 5).first().catskill
    skills_page_webser = Category.query.filter(
        Category.id == 6).first().catskill
    skills_page_message = Category.query.filter(
        Category.id == 7).first().catskill
    skills_page_os = Category.query.filter(
        Category.id == 8).first().catskill
    skills_page_vcs = Category.query.filter(
        Category.id == 9).first().catskill
    skills_page_virt = Category.query.filter(
        Category.id == 10).first().catskill
    skills_page_auto = Category.query.filter(
        Category.id == 11).first().catskill
    skills_page_orm = Category.query.filter(
        Category.id == 12).first().catskill
    skills_page_spm = Category.query.filter(
        Category.id == 13).first().catskill
    skills_page_mpm = Category.query.filter(
        Category.id == 14).first().catskill
    skills_page_monitor = Category.query.filter(
        Category.id == 15).first().catskill

    return render_template('profile/profile.html', page_title=title, form=form, user=user, skills_base=skills_base,
                           areas_base=areas_base, area_page=area_page, skills_page_lang=skills_page_lang,
                           skills_page_db=skills_page_db, skills_page_frame=skills_page_frame,
                           skills_page_webprot=skills_page_webprot, skills_page_search=skills_page_search,
                           skills_page_webser=skills_page_webser, skills_page_message=skills_page_message,
                           skills_page_os=skills_page_os, skills_page_vcs=skills_page_vcs,
                           skills_page_virt=skills_page_virt, skills_page_auto=skills_page_auto,
                           skills_page_orm=skills_page_orm, skills_page_spm=skills_page_spm,
                           skills_page_mpm=skills_page_mpm, skills_page_monitor=skills_page_monitor)

@blueprint.route('/process-save-changes-person', methods=['POST'])
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
    return redirect(url_for('profile.profile'))

@blueprint.route('/profile/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    title = "Избранные вакансии"
    favourites = Favourite.query.filter(
        Favourite.user_id == current_user.id).all()
    return render_template('profile/favourite.html', page_title=title, favourites=favourites)

@blueprint.route('/process-favourite/<int:id>', methods=['GET', 'POST'])
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

    return redirect(url_for('profile.profile'))

@blueprint.route('/process-delete/<int:id>', methods=['GET', 'POST'])
@login_required
def process_delete(id):
    favourite = Favourite.query.get_or_404(id)
    db.session.delete(favourite)
    db.session.commit()
    flash('Вакансия удалена из избранного')

    return redirect(url_for('profile.favourite'))

@blueprint.route('/profile/change_password')
@login_required
def change_password():
    form = ChangePasswordForm()
    title = 'Изменить пароль'
    return render_template('profile/change_password.html', page_title=title, form=form)

@blueprint.route('/process-change-password', methods=['POST'])
@login_required
def process_change_password():
    form = ChangePasswordForm()
    user = User.query.filter(
        User.username == current_user.username).first()
    if form.validate_on_submit() and user.check_password(form.old_password.data):
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Пароль изменен')
        return redirect(url_for('profile.profile'))

    else:
        if not user.check_password(form.old_password.data):
            flash('Неправильный текущий пароль')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле {}: {}'.format(
                        getattr(form, field).label.text, error))

    return redirect(url_for('profile.change_password'))

@blueprint.route('/profile/relevant_vacancies')
@login_required
def relevant_vacancies():

    title = "Подходящие вакансии"
    user = User.query.filter(User.id == current_user.id).first()
    page = request.args.get('page', 1, type=int)
    skills_base = user.user_skill
    areas_base = user.user_area

    skills = [skill.id for skill in skills_base]
    areas = [area.id for area in areas_base]

    if skills or areas:
        vacancies = Vacancy.query.filter(or_(
            (Vacancy.vacancy_prof_area == area.id for area in areas_base))).filter(or_(
                *[Vacancy.vacancy_text_clean.ilike('%' + (skill.name) + '%') for skill in skills_base])).filter(
            Vacancy.vacancy_prof_area != None).paginate(page=page, per_page=20)

    else:
        vacancies = []

    favourite = Favourite.query.filter(
        Favourite.user_id == current_user.id).all()
    favourite_vacancy = []
    for favour in favourite:
        favourite_vacancy.append(favour.vacancy_id)

    return render_template('profile/relevant_vacancies.html', page_title=title, vacancies=vacancies,
                           favourite=favourite_vacancy)

@blueprint.route('/process-save-change-skills', methods=['POST'])
@login_required
def process_save_change_skills():
    user = User.query.filter(User.id == current_user.id).first()
    skills_user = get_user_skills_from_database(user)
    areas_user = get_user_areas_from_database(user)

    areas = get_areas()
    skills_lang = get_skills_lang()
    skills_db = get_skills_db()
    skills_frame = get_skills_frame()
    skills_webprot = get_skills_webprot()
    skills_search = get_skills_search()
    skills_webser = get_skills_webser()
    skills_message = get_skills_message()
    skills_os = get_skills_os()
    skills_vcs = get_skills_vcs()
    skills_virt = get_skills_virt()
    skills_auto = get_skills_auto()
    skills_orm = get_skills_orm()
    skills_spm = get_skills_spm()
    skills_mpm = get_skills_mpm()
    skills_monitor = get_skills_monitor()

    if request.form:
        areas_page = request.form.getlist("areas")
        skills_page_lang = request.form.getlist("skills_lang")
        skills_page_db = request.form.getlist("skills_db")
        skills_page_frame = request.form.getlist("skills_frame")
        skills_page_webprot = request.form.getlist("skills_webprot")
        skills_page_search = request.form.getlist("skills_search")
        skills_page_webser = request.form.getlist("skills_webser")
        skills_page_message = request.form.getlist("skills_message")
        skills_page_os = request.form.getlist("skills_os")
        skills_page_vcs = request.form.getlist("skills_vcs")
        skills_page_virt = request.form.getlist("skills_virt")
        skills_page_auto = request.form.getlist("skills_auto")
        skills_page_orm = request.form.getlist("skills_orm")
        skills_page_spm = request.form.getlist("skills_spm")
        skills_page_mpm = request.form.getlist("skills_mpm")
        skills_page_monitor = request.form.getlist("skills_monitor")

        update_user_areas(areas_user, areas, areas_page, user)
        update_user_skills(skills_user, skills_lang,skills_page_lang, user)
        update_user_skills(skills_user, skills_db, skills_page_db, user)
        update_user_skills(skills_user, skills_frame,skills_page_frame, user)
        update_user_skills(skills_user, skills_webprot,skills_page_webprot, user)
        update_user_skills(skills_user, skills_search,skills_page_search, user)
        update_user_skills(skills_user, skills_webser,skills_page_webser, user)
        update_user_skills(skills_user, skills_message,skills_page_message, user)
        update_user_skills(skills_user, skills_os, skills_page_os, user)
        update_user_skills(skills_user, skills_vcs, skills_page_vcs, user)
        update_user_skills(skills_user, skills_virt,skills_page_virt, user)
        update_user_skills(skills_user, skills_auto,skills_page_auto, user)
        update_user_skills(skills_user, skills_orm, skills_page_orm, user)
        update_user_skills(skills_user, skills_spm, skills_page_spm, user)
        update_user_skills(skills_user, skills_mpm, skills_page_mpm, user)
        update_user_skills(skills_user, skills_monitor,skills_page_monitor, user)

    flash('Изменения сохранены')
    return redirect(url_for('profile.profile'))
