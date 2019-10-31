import json
from webapp.model import db, Category, Skill


def get_category():
    filename = 'data/CategorySkills.json'
    with open(filename, 'r', encoding='utf-8') as f:
        reader = json.load(f)

    for row in reader:
        for key, value in row.items():
            category = key
            save_category(category)

    return False


def get_skills():
    filename = 'data/CategorySkills.json'
    with open(filename, 'r', encoding='utf-8') as f:
        reader = json.load(f)

    for row in reader:
        for key, values in row.items():
            category = key
            for value in values:
                skill = value
                save_skill(category, skill)


def save_category(category):
    category_exists = Category.query.filter(Category.category == category).count()
    if not category_exists:
        category_add = Category(category=category)
        db.session.add(category_add)
        db.session.commit()

    skill_exists = Skill.query.filter(Skill.skill == skill).count()
    if not skill_exists:
        skill_add = Skill(category=category, skill=skill)
        db.session.add(skill_add)
        db.session.commit()
