from webapp.db import db


class Favourite(db.Model):
    __tablename__ = "favourite_vacancies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey(
        'vacancies.id'), nullable=False)
