import json
from webapp import create_app
from webapp.model import Skill, Category, db

app = create_app()

def save_skill(skill_):
    app = create_app()
    with app.app_context():
        skill_add = Skill()
        skill_add.skill = skill_
        db.session.add(skill_add)
        db.session.commit()


def save_category(category_):
    app = create_app()
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

with app.app_context():


