from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    new_password = PasswordField('Новый пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    new_password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('new_password')],
                                  render_kw={"class": "form-control"})
    submit = SubmitField('Изменить', render_kw={"class": "btn btn-primary"})


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
