from webapp.vacancy.models import db, Category, Skill, ProfessionalArea
from webapp.user.models import User


def get_user_skills_from_database(user):
    skills_base = user.user_skill
    skills_user = []
    for skill_base in skills_base:
        skills_user.append(skill_base.id)
    return skills_user

def get_user_areas_from_database(user):
    areas_base = user.user_area
    areas_user = []
    for area_base in areas_base:
        areas_user.append(area_base.id)
    return areas_user

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

def update_user_areas(areas_user, areas, areas_page, user):
    for area in areas:
        if (area not in areas_user) and (str(area) in areas_page):
            area_add = ProfessionalArea.query.filter(ProfessionalArea.id == area).first()
            area_add.user.append(user)
            db.session.commit()
        elif (area in areas_user) and (str(area) not in areas_page):
            area_delete = ProfessionalArea.query.filter(ProfessionalArea.id == area).first()
            area_delete.user.remove(user)
            db.session.commit()
    return False

def get_areas():
    areas = ProfessionalArea.query.all()
    areas_get = []
    for area in areas:
        areas_get.append(area.id)
    return areas_get

def get_skills_lang():
    skills = Category.query.filter(Category.id == 1).first().catskill
    skills_lang = []
    for skill in skills:
        skills_lang.append(skill.id)
    return skills_lang

def get_skills_db():
    skills = Category.query.filter(Category.id == 2).first().catskill
    skills_db = []
    for skill in skills:
        skills_db.append(skill.id)
    return skills_db

def get_skills_frame():
    skills = Category.query.filter(Category.id == 3).first().catskill
    skills_frame = []
    for skill in skills:
        skills_frame.append(skill.id)
    return skills_frame

def get_skills_webprot():
    skills = Category.query.filter(Category.id == 4).first().catskill
    skills_webprot = []
    for skill in skills:
        skills_webprot.append(skill.id)
    return skills_webprot

def get_skills_search():
    skills = Category.query.filter(Category.id == 5).first().catskill
    skills_search = []
    for skill in skills:
        skills_search.append(skill.id)
    return skills_search

def get_skills_webser():
    skills = Category.query.filter(Category.id == 6).first().catskill
    skills_webser = []
    for skill in skills:
        skills_webser.append(skill.id)
    return skills_webser

def get_skills_message():
    skills = Category.query.filter(Category.id == 7).first().catskill
    skills_message = []
    for skill in skills:
        skills_message.append(skill.id)
    return skills_message

def get_skills_os():
    skills = Category.query.filter(Category.id == 8).first().catskill
    skills_os = []
    for skill in skills:
        skills_os.append(skill.id)
    return skills_os

def get_skills_vcs():
    skills = Category.query.filter(Category.id == 9).first().catskill
    skills_vcs = []
    for skill in skills:
        skills_vcs.append(skill.id)
    return skills_vcs

def get_skills_virt():
    skills = Category.query.filter(Category.id == 10).first().catskill
    skills_virt = []
    for skill in skills:
        skills_virt.append(skill.id)
    return skills_virt

def get_skills_auto():
    skills = Category.query.filter(Category.id == 11).first().catskill
    skills_auto = []
    for skill in skills:
        skills_auto.append(skill.id)
    return skills_auto

def get_skills_orm():
    skills = Category.query.filter(Category.id == 12).first().catskill
    skills_orm = []
    for skill in skills:
        skills_orm.append(skill.id)
    return skills_orm

def get_skills_spm():
    skills = Category.query.filter(Category.id == 13).first().catskill
    skills_spm = []
    for skill in skills:
        skills_spm.append(skill.id)
    return skills_spm

def get_skills_mpm():
    skills = Category.query.filter(Category.id == 14).first().catskill
    skills_mpm = []
    for skill in skills:
        skills_mpm.append(skill.id)
    return skills_mpm

def get_skills_monitor():
    skills = Category.query.filter(Category.id == 15).first().catskill
    skills_monitor = []
    for skill in skills:
        skills_monitor.append(skill.id)
    return skills_monitor
