from webapp import create_app
from webapp.category_skills_to_db import get_category, get_skills
from webapp.model import HeadHunterVacancy

app = create_app()
with app.app_context():
    vacancies = HeadHunterVacancy.query.all()
    requirements_text = []
    for v in vacancies:
        requirements_text.append(v)
    get_category()
    get_skills(requirements_text)
