from flask import Flask, render_template, flash, redirect, url_for, request
from flask import Blueprint
from flask_login import current_user, login_required
from sqlalchemy import or_


from webapp.vacancy.models import Vacancy, Skill, Category, ProfessionalArea
from webapp.user.models import User
from webapp.profile.models import Favourite
from webapp.db import db

blueprint = Blueprint('vacancy', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    title = "Вакансии для разработчиков"
    page = request.args.get('page', 1, type=int)
    vacancies = Vacancy.query.filter(
        Vacancy.vacancy_prof_area != None).paginate(page=page, per_page=20)
    skills = Skill.query.all()
    categories = Category.query.all()
    areas = ProfessionalArea.query.all()

    if current_user.is_authenticated:
        favourite = Favourite.query.filter(
            Favourite.user_id == current_user.id).all()
        favourite_vacancy = []
        for favour in favourite:
            favourite_vacancy.append(favour.vacancy_id)
        return render_template('vacancy/index.html', page_title=title, vacancies=vacancies, favourite=favourite_vacancy,
                               skills=skills, categories=categories, areas=areas)
    else:
        return render_template('vacancy/index.html', page_title=title, vacancies=vacancies,  skills=skills,
                               categories=categories, areas=areas)

@blueprint.route('/search')
def search():
    title = "Вакансии для разработчиков"
    page = request.args.get('page', 1, type=int)
    areas = ProfessionalArea.query.all()
    skills = Skill.query.all()
    categories = Category.query.all()

    areas_page = [int(item) for item in request.args.getlist('areas')]
    skills_page = [int(item) for item in request.args.getlist('skills')]

    if request.method == 'GET':
        print(areas_page)
        print(skills_page)

        skills_names = Skill.query.filter(
            or_(Skill.id == skill_page for skill_page in skills_page)).all()

        vacancies = Vacancy.query.filter(or_(
            (Vacancy.vacancy_prof_area == area_page for area_page in areas_page))).filter(or_(
            *[Vacancy.vacancy_text_clean.ilike('%' + (skill.name) + '%') for skill in skills_names])).filter(
            Vacancy.vacancy_prof_area != None).paginate(page=page, per_page=20)

        if current_user.is_authenticated:
            favourite = Favourite.query.filter(
                Favourite.user_id == current_user.id).all()
            favourite_vacancy = []
            for favour in favourite:
                favourite_vacancy.append(favour.vacancy_id)
            return render_template('vacancy/index.html', page_title=title, vacancies=vacancies, favourite=favourite_vacancy,
                                   skills=skills, categories=categories, areas=areas, areas_page=areas_page,
                                   skills_page=skills_page)
        else:
            return render_template('vacancy/index.html', page_title=title, vacancies=vacancies, skills=skills,
                                   categories=categories, areas=areas, areas_page=areas_page, skills_page=skills_page)

    return False
