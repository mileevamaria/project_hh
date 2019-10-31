from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


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
    company_url = db.Column(db.TEXT, nullable=True)
    vacancy_adress = db.Column(db.TEXT, nullable=True)
    vacancy_expirience = db.Column(db.TEXT, nullable=True)
    vacancy_employment_type = db.Column(db.TEXT, nullable=True)
    vacancy_text_dirty = db.Column(db.TEXT, nullable=True)
    vacancy_text_clean = db.Column(db.TEXT, nullable=True)
    vacancy_key_skills = db.Column(db.TEXT, nullable=True)
    industry = db.Column(db.TEXT, nullable=True)
    lang = db.Column(db.String(5), nullable=True)
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
    vacancy_published_at = db.Column(db.TIMESTAMP, nullable=True)
    parsed_at = db.Column(db.TIMESTAMP, server_default=func.now())

    favourites = db.relationship('Favourite', backref='vacancy_favourite')
    grade = db.relationship('VacancyGrade', backref='vacancy_grade')


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    first_name = db.Column(db.String(80), nullable=True, server_default='Имя')
    last_name = db.Column(db.String(80), nullable=True, server_default='Фамилия')
    city = db.Column(db.String(80), nullable=True, server_default='Город')
    favourites = db.relationship('Favourite', backref='user_favourite')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.TEXT, nullable=False)
    skills = db.relationship('Skill', backref='category_skill')


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.TEXT, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    count = db.Column(db.Integer, nullable=True)


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.TEXT, nullable=False)
    vacancies = db.relationship('VacancyGrade', backref='specialization_grade')


class Favourite(db.Model):
    __tablename__ = "favourite_vacancies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancies.id'), nullable=False)


class VacancyGrade(db.Model):
    __tablename__ = "vacancies_grade"

    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancies.id'), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)
