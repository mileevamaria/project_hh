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
    vacancy_expirience = db.Column(db.TEXT, nullable=True)
    vacancy_employment_type = db.Column(db.TEXT, nullable=True)
    vacancy_text_clean = db.Column(db.TEXT, nullable=True)
    vacancy_text_en = db.Column(db.TEXT, nullable=True)
    vacancy_key_skills = db.Column(db.TEXT, nullable=True)
    industry = db.Column(db.TEXT, nullable=True)
    language = db.Column(db.String(5), nullable=True)
    vacancy_published_at = db.Column(db.TEXT, nullable=True)
    vacancy_graded = db.Column(db.Boolean, default=0, nullable=False)

    favourites = db.relationship('Favourite', backref='vacancy_favourite')

assoc_skill_user = db.Table("assoc_skill_user",
                        db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                        db.Column("skill_id", db.Integer, db.ForeignKey("skills.id")))


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
    user = db.relationship('Skill', secondary=assoc_skill_user, backref=db.backref('user', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Favourite(db.Model):
    __tablename__ = "favourite_vacancies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancies.id'), nullable=False)


assoc_skill_category = db.Table("assoc_skill_category",
                       db.Column("skill_id", db.Integer, db.ForeignKey("skills.id")),
                       db.Column("category_id", db.Integer, db.ForeignKey("categories.id")))


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.relationship('Category', secondary=assoc_skill_category, backref=db.backref('catskills', lazy='dynamic'))

class Statistic(db.Model):
    __tablename__ = "statistic"

    id = db.Column(db.Integer, primary_key=True)
    vacancy_count = db.Column(db.Integer, nullable=True)
    languages = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.TIMESTAMP)