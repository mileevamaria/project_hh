from webapp.db import db


class Statistic(db.Model):
    __tablename__ = "statistic"

    id = db.Column(db.Integer, primary_key=True)
    vacancy_count = db.Column(db.Integer, nullable=True)
    languages = db.Column(db.TEXT, nullable=True)
    grades = db.Column(db.TEXT, nullable=True)
    ungraded_vacancies = db.Column(db.TEXT, nullable=True)
    words = db.Column(db.TEXT, nullable=True)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
