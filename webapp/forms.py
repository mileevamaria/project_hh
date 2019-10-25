from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from webapp.model import Skills


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})


class ProfileForm(FlaskForm):
    username = StringField('Никнейм', render_kw={"class": "form-control", "readonly": ''})
    first_name = StringField('Имя', render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', render_kw={"class": "form-control"})
    city = StringField('Город', render_kw={"class": "form-control"})
    change = SubmitField('Изменить', render_kw={"class": "btn btn-link btn-sm"})
    favourite = SubmitField('Избранные вакансии', render_kw={"class": "btn btn-link btn-lg"})
    relevant = SubmitField('Посмотреть подходящие вакансии', render_kw={"class": "btn btn-link btn-lg"})
    change_password = SubmitField('Изменить пароль', render_kw={"class": "btn btn-link btn-lg"})
    save_changes = SubmitField('Сохранить изменения', render_kw={"class": "btn btn-primary"})


class VacancyForm(FlaskForm):
    title = StringField('Название вакансии', validators=[DataRequired()])
    published = StringField('Дата публикации', validators=[DataRequired()])
    requirements_text = StringField('Требования', validators=[DataRequired()])
    url = StringField('Ссылка на вакансию', validators=[DataRequired()])
    favourite = SubmitField('Добавить в избранное', render_kw={"class": "btn btn-warning btn-sm"})


class SkillsForm(FlaskForm):
    skills_nosql = QuerySelectField('Базы NoSQL',
                                    query_factory=lambda: Skills.query.filter(
                                        Skills.category == 'Базы данных NoSQL').all(),
                                    get_label="skill")