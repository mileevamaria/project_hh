from sqlalchemy.sql import func

from webapp.user.models import assoc_area_user, assoc_skill_user
from webapp.db import db


class Vacancy(db.Model):
    __tablename__ = "vacancies"

    id = db.Column(db.Integer, primary_key=True)
    vacancy_url = db.Column(db.TEXT, nullable=True)
    vacancy_name = db.Column(db.TEXT, nullable=True)
    vacancy_city = db.Column(db.String(50), nullable=True)
    vacancy_country = db.Column(db.String(10), nullable=True)
    vacancy_salary_value = db.Column(db.TEXT, nullable=True)
    vacancy_salary_min = db.Column(db.TEXT, nullable=True)
    vacancy_salary_max = db.Column(db.TEXT, nullable=True)
    vacancy_salary_currency = db.Column(db.TEXT, nullable=True)
    vacancy_salary_period = db.Column(db.TEXT, nullable=True)
    company_name = db.Column(db.TEXT, nullable=True)
    vacancy_expirience = db.Column(db.TEXT, nullable=True)
    vacancy_employment_type = db.Column(db.TEXT, nullable=True)
    vacancy_text_clean = db.Column(db.TEXT, nullable=True)
    vacancy_text_en = db.Column(db.TEXT, nullable=True)
    vacancy_key_skills = db.Column(db.TEXT, nullable=True)
    industry = db.Column(db.TEXT, nullable=True)
    language = db.Column(db.String(5), nullable=True)
    vacancy_published_at = db.Column(db.TEXT, nullable=True)
    vacancy_graded = db.Column(db.Boolean, default=0, nullable=False)
    vacancy_prof_area = db.Column(db.Integer, nullable=True)

    favourites = db.relationship('Favourite', backref='vacancy_favourite')
    vacancy_grades = db.relationship(
        'VacancyGrade', backref='vacancy_grades', lazy=True)


assoc_skill_category = db.Table("assoc_skill_category",
                                db.Column("skill_id", db.Integer,
                                          db.ForeignKey("skills.id")),
                                db.Column("category_id", db.Integer, db.ForeignKey("categories.id")))


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    count = db.Column(db.Integer, nullable=True)
    category = db.relationship('Category', secondary=assoc_skill_category, backref=db.backref('catskill', lazy='dynamic'))
    skill = db.relationship('User', secondary=assoc_skill_user, backref=db.backref('user_skill', lazy='dynamic'))


class ProfessionalArea(db.Model):
    __tablename__ = "prof_areas"

    id = db.Column(db.Integer, primary_key=True)
    area_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    count = db.Column(db.Integer, nullable=True)

    prof_grades = db.relationship(
        'VacancyGrade', backref='prof_grades', lazy=True)
    area = db.relationship('User', secondary=assoc_area_user,
                           backref=db.backref('user_area', lazy='dynamic'))


class VacancyGrade(db.Model):
    __tablename__ = "vacancy_grades"

    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey(
        'vacancies.id'), nullable=False)
    prof_area_id = db.Column(db.Integer, db.ForeignKey(
        'prof_areas.id'), nullable=False)
    grade = db.Column(db.DECIMAL(18, 17), nullable=True)


class SpyderVacancies(db.Model):
    __tablename__ = 'vacancies_spyder'

    id = db.Column(db.Integer, primary_key=True)
    vacancy_url = db.Column(db.TEXT, nullable=True)
    vacancy_name = db.Column(db.TEXT, nullable=True)
    vacancy_city = db.Column(db.String(50), nullable=True)
    vacancy_country = db.Column(db.String(10), nullable=True)
    vacancy_salary_value = db.Column(db.TEXT, nullable=True)
    vacancy_salary_min = db.Column(db.TEXT, nullable=True)
    vacancy_salary_max = db.Column(db.TEXT, nullable=True)
    vacancy_salary_currency = db.Column(db.TEXT, nullable=True)
    vacancy_salary_period = db.Column(db.TEXT, nullable=True)
    company_name = db.Column(db.TEXT, nullable=True)
    company_url = db.Column(db.TEXT, nullable=True)
    vacancy_adress = db.Column(db.TEXT, nullable=True)
    vacancy_expirience = db.Column(db.TEXT, nullable=True)
    vacancy_employment_type = db.Column(db.TEXT, nullable=True)
    vacancy_text_dirty = db.Column(db.TEXT, nullable=True)
    vacancy_text_clean = db.Column(db.TEXT, nullable=True)
    vacancy_key_skills = db.Column(db.TEXT, nullable=True)
    industry = db.Column(db.TEXT, nullable=True)
    language = db.Column(db.String(5), nullable=True)
    task_idx = db.Column(db.TEXT, nullable=True)
    requirements_idx = db.Column(db.TEXT, nullable=True)
    company_offer_idx = db.Column(db.TEXT, nullable=True)
    will_plus_idx = db.Column(db.TEXT, nullable=True)
    common_idx = db.Column(db.TEXT, nullable=True)
    task_text_value = db.Column(db.TEXT, nullable=True)
    task_text = db.Column(db.TEXT, nullable=True)
    requirements_text_value = db.Column(db.TEXT, nullable=True)
    requirements_text = db.Column(db.TEXT, nullable=True)
    company_offer_text_value = db.Column(db.TEXT, nullable=True)
    company_offer_text = db.Column(db.TEXT, nullable=True)
    will_plus_text_value = db.Column(db.TEXT, nullable=True)
    will_plus_text = db.Column(db.TEXT, nullable=True)
    vacancy_published_at = db.Column(db.TEXT, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
