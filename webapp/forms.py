from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.model import Skill, User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    first_name = StringField('Имя', render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', render_kw={"class": "form-control"})
    city = StringField('Город', render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с такой почтой уже существует')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    new_password = PasswordField('Новый пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    new_password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('new_password')],
                                  render_kw={"class": "form-control"})
    submit = SubmitField('Изменить пароль!', render_kw={"class": "btn btn-primary"})


class ProfileForm(FlaskForm):
    username = StringField('Никнейм', render_kw={"class": "form-control", "readonly": ''})
    email = StringField('Почта', render_kw={"class": "form-control", "readonly": ''})
    first_name = StringField('Имя', render_kw={"class": "form-control"})
    last_name = StringField('Фамилия', render_kw={"class": "form-control"})
    city = StringField('Город', render_kw={"class": "form-control"})
    favourite = SubmitField('Избранные вакансии', render_kw={"class": "btn btn-link btn-lg"})
    relevant = SubmitField('Посмотреть подходящие вакансии', render_kw={"class": "btn btn-link btn-lg"})
    change_password = SubmitField('Изменить пароль', render_kw={"class": "btn btn-link btn-lg"})
    save_changes = SubmitField('Сохранить изменения', render_kw={"class": "btn btn-primary"})


class SkillsForm(FlaskForm):
    skills_nosql = QuerySelectField('Базы NoSQL',
                                    query_factory=lambda: Skill.query.filter(
                                        Skill.category == 'Базы данных NoSQL').all(),
                                    get_label="skill")


