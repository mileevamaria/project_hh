from webapp.model import db, Category, Skill


def get_user_skills_from_database(user):
    skills_base = user.user_skill
    skills_user = []
    for skill_base in skills_base:
        skills_user.append(skill_base.id)

    return skills_user


def update_user_skills(skills_user, skills_category, skills_page, user):
    for skill_category in skills_category:
        if (skill_category not in skills_user) and (str(skill_category) in skills_page):
            skill_add = Skill.query.filter(Skill.id == skill_category).first()
            skill_add.user.append(user)
            db.session.commit()
        elif (skill_category in skills_user) and (str(skill_category) not in skills_page):
            skill_delete = Skill.query.filter(Skill.id == skill_category).first()
            skill_delete.user.remove(user)
            db.session.commit()

    return False


def get_skills_nosql():
    skills = Category.query.filter(Category.id == 1).first().catskill
    skills_nosql = []
    for skill in skills:
        skills_nosql.append(skill.id)

    return skills_nosql

def get_skills_sql():
    skills = Category.query.filter(Category.id == 2).first().catskill
    skills_sql = []
    for skill in skills:
        skills_sql.append(skill.id)

    return skills_sql
