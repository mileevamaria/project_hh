import json, re
from webapp import create_app
from webapp.model import Skill, Category, db, User, Vacancy, VacancyGrade
from datetime import datetime
from sqlalchemy import or_

app = create_app()

def save_skill(skill_):
    with app.app_context():
        skill_add = Skill()
        skill_add.skill = skill_
        db.session.add(skill_add)
        db.session.commit()


def save_category(category_):
    with app.app_context():
        category_add = Category()
        category_add.category = category_
        db.session.add(category_add)
        db.session.commit()


def get_category_skill():
    filename = 'data/CategorySkills.json'
    with open(filename, 'r', encoding='utf-8') as f:
        reader = json.load(f)

        for elements in reader:
            for category_, skills in elements.items():
                save_category(category_)
                for skill_ in skills:
                    save_skill(skill_)


def something():
    with app.app_context():
        user = User.query.filter(User.id == 1).first()
        user_skills = user.user_skill
        skills = Category.query.filter(Category.id == 1).first().catskills
        for skill in skills:
            print(skill.name)
        print('_____________')
        for skill in user_skills:
            print(skill.name)

def vacancy_data():
    with app.app_context():
        vacancies = Vacancy.query.all()
        for vacancy in vacancies:
            if len(vacancy.vacancy_published_at) != 10:
                vacancy_edit = re.sub('T', ' ', vacancy.vacancy_published_at)
                vacancy_edit = vacancy_edit[:-10]
                vacancy_time = datetime.strptime(vacancy_edit, "%Y-%m-%d %H:%M:%S")
                vacancy_time = vacancy_time.strftime("%d-%m-%Y")
                vacancy.vacancy_published_at = vacancy_time
                db.session.commit()
    return False

def vacancy_grade():
    with app.app_context():
        vacancies = Vacancy.query.all()
        for vacancy in vacancies:
            grades = VacancyGrade.query.filter(VacancyGrade.vacancy_id == vacancy.id).all()

            max_grades = []
            for gr in grades:
                max_grades.append(gr.grade)

            max_grade = VacancyGrade.query.filter(VacancyGrade.vacancy_id == vacancy.id,
                                                  VacancyGrade.grade == max(max_grades)).first()

            if max(max_grades) > 0.5:
                vacancy.vacancy_prof_area = max_grade.prof_area_id
                db.session.commit()
    return False


with app.app_context():
    areas_page = [1, 2]
    skills_page = [11, 21]
    skills = Skill.query.filter(or_(Skill.id == skill_page for skill_page in skills_page)).all()

    vacancies = Vacancy.query.filter(or_(
        (Vacancy.vacancy_prof_area == area_page for area_page in areas_page))).filter(or_(
        *[Vacancy.vacancy_text_clean.ilike('%' + (skill.name) + '%') for skill in skills])).all()

    for vacancy in vacancies:
        if vacancy.id <= 100:
            print(vacancy.id)





