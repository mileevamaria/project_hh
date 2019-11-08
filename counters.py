from webapp.model import Skill, Category, db, User, Vacancy, ProfessionalArea
from sqlalchemy import or_
from webapp import create_app

app = create_app()

def count_skills():
    with app.app_context():
        vacancies = Vacancy.query.all()
        skills = Skill.query.all()
        for skill in skills:
            skill.count = 0
            db.session.commit()

        for vacancy in vacancies:
            for skill in skills:
                if skill.name.lower() in vacancy.vacancy_text_clean.lower():
                    skill.count += 1
                    db.session.commit()
    return False

def count_areas():
    with app.app_context():
        vacancies = Vacancy.query.all()
        areas = ProfessionalArea.query.all()
        for area in areas:
            area.count = 0
            db.session.commit()

        for vacancy in vacancies:
            for area in areas:
                if vacancy.vacancy_prof_area == area.id:
                    area.count += 1
                    db.session.commit()
    return False


count_areas()
