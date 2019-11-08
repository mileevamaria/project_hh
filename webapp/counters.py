from webapp.model import Skill, Category, db, User, Vacancy, ProfessionalArea

def count_skills():
    vacancies = Vacancy.query.all()
    skills = Skill.query.all()
    for skill in skills:
        if skill.count != 0:
            skill.count = 0
            db.session.commit()

    for vacancy in vacancies:
        for skill in skills:
            if skill.name.lower() in vacancy.vacancy_text_clean.lower():
                skill.count += 1
                db.session.commit()

    return False

def count_areas():
    vacancies = Vacancy.query.all()
    areas = ProfessionalArea.query.all()
    for area in areas:
        if area.count != 0:
            area.count = 0
            db.session.commit()

    for vacancy in vacancies:
        for area in areas:
            if vacancy.vacancy_prof_area == area.id:
                area.count += 1
                db.session.commit()


    return False